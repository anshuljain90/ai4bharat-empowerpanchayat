from typing import List, Optional
import requests
import json
import os
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# Map display language names to ISO 639-1 codes used by Whisper
LANGUAGE_CODE_MAP = {
    "english": "en", "hindi": "hi", "gujarati": "gu", "marathi": "mr",
    "telugu": "te", "bengali": "bn", "kannada": "kn", "malayalam": "ml",
    "tamil": "ta", "spanish": "es", "german": "de", "italian": "it",
    "french": "fr", "urdu": "ur", "punjabi": "pa", "assamese": "as",
    "oriya": "or", "arabic": "ar", "russian": "ru", "portuguese": "pt",
    "korean": "ko", "turkish": "tr", "thai": "th", "vietnamese": "vi",
    "dutch": "nl", "polish": "pl", "malay": "ms", "tagalog": "tl",
    "indonesian": "id", "chinese": "zh",
}

class STTTranscriber:
    """HuggingFace Whisper STT Transcriber"""

    def __init__(self):
        self.api_key = settings.HF_TOKEN
        self.endpoint = settings.STT_MODEL_ENDPOINT
        logger.info(f"STT Transcriber initialized: {bool(self.api_key)}")

    def _resolve_language_code(self, language: Optional[str]) -> Optional[str]:
        """Convert a language name or code to the ISO 639-1 code Whisper expects."""
        if not language:
            return None
        lang = language.strip().lower()
        # Already a short code
        if lang in LANGUAGE_CODE_MAP.values():
            return lang
        return LANGUAGE_CODE_MAP.get(lang)

    def transcribe_audio(self, audio_file_path: str, language: Optional[str] = None) -> str:
        """Transcribe audio using HuggingFace Whisper API with optional language hint."""
        try:
            if not self.api_key or not self.endpoint:
                logger.error("HuggingFace API not configured")
                return ""

            with open(audio_file_path, "rb") as f:
                audio_data = f.read()

            lang_code = self._resolve_language_code(language)

            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }

            logger.info(
                f"Sending {len(audio_data)} bytes to {self.endpoint} "
                f"(language hint: {lang_code or 'auto-detect'})"
            )

            # Use multipart form so we can pass parameters alongside the audio
            files = {"file": (os.path.basename(audio_file_path), audio_data, self._get_content_type(audio_file_path))}
            payload = {}
            if lang_code:
                payload["language"] = lang_code

            # Try multipart with parameters first
            response = requests.post(
                self.endpoint,
                headers=headers,
                files=files,
                data=payload,
                timeout=180,
            )

            # Fallback: if the endpoint rejects multipart, retry with raw bytes
            if response.status_code not in (200, 201):
                logger.warning(f"Multipart request failed ({response.status_code}), retrying with raw audio bytes")
                headers["Content-Type"] = self._get_content_type(audio_file_path)
                response = requests.post(
                    self.endpoint,
                    headers=headers,
                    data=audio_data,
                    timeout=180,
                )

            if response.status_code == 200:
                result = response.json()
                transcription = result.get("text", "") if isinstance(result, dict) else ""
                logger.info(f"Whisper transcription successful (length: {len(transcription)} chars).")
                return transcription.strip()

            logger.error(f"Whisper API error: {response.status_code} - {response.text}")
            return ""

        except Exception as e:
            logger.error(f"Transcription failed: {e}", exc_info=True)
            return ""

    def _get_content_type(self, file_path: str) -> str:
        """Get content type based on file extension"""
        ext = os.path.splitext(file_path)[1].lower()
        return {
            '.wav': 'audio/wav',
            '.mp3': 'audio/mpeg',
            '.flac': 'audio/flac',
            '.m4a': 'audio/mp4',
            '.ogg': 'audio/ogg'
        }.get(ext, 'audio/wav') # Default to wav if unknown

# Global instance
stt_transcriber = STTTranscriber()