import hashlib
import logging
from typing import Optional
import boto3
from botocore.exceptions import ClientError
from app.core.config import settings

logger = logging.getLogger(__name__)


class TTSService:
    """Text-to-Speech service using Amazon Polly with S3 caching.

    Polly voice reference (ap-south-1):
      - Aditi:   hi-IN, standard  (Hindi female — widely available)
      - Kajal:   en-IN, neural/generative (English-Indian female)
      - Raveena: en-IN, standard  (English-Indian female)

    For Hindi TTS we use Aditi (standard) because:
      - It's the only Hindi voice available in all regions
      - Neural Hindi voices are not available in ap-south-1
    """

    # voice_id, engine, language_code
    VOICE_CONFIG = {
        "hi":      ("Aditi", "standard", "hi-IN"),
        "hindi":   ("Aditi", "standard", "hi-IN"),
        "en":      ("Raveena", "standard", "en-IN"),
        "english": ("Raveena", "standard", "en-IN"),
        # Regional languages — fall back to Hindi Aditi
        "ta":      ("Aditi", "standard", "hi-IN"),
        "te":      ("Aditi", "standard", "hi-IN"),
        "bn":      ("Aditi", "standard", "hi-IN"),
        "mr":      ("Aditi", "standard", "hi-IN"),
        "gu":      ("Aditi", "standard", "hi-IN"),
        "kn":      ("Aditi", "standard", "hi-IN"),
        "ml":      ("Aditi", "standard", "hi-IN"),
    }

    DEFAULT_VOICE = ("Aditi", "standard", "hi-IN")

    def __init__(self):
        self.polly_client = None
        self.s3_client = None
        self._init_clients()

    def _init_clients(self):
        try:
            kwargs = {"region_name": settings.AWS_REGION}
            if settings.AWS_ACCESS_KEY_ID:
                kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
                kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
            self.polly_client = boto3.client("polly", **kwargs)
            self.s3_client = boto3.client("s3", **kwargs)
            logger.info("[TTS] Polly and S3 clients initialized")
        except Exception as e:
            logger.error(f"[TTS] Failed to initialize clients: {e}")

    def _cache_key(self, text: str, language: str) -> str:
        content_hash = hashlib.sha256(f"{text}:{language}".encode()).hexdigest()
        return f"tts-cache/{language}/{content_hash}.mp3"

    def _check_cache(self, cache_key: str) -> Optional[bytes]:
        try:
            response = self.s3_client.get_object(
                Bucket=settings.S3_BUCKET, Key=cache_key
            )
            logger.info(f"[TTS] Cache hit: {cache_key}")
            return response["Body"].read()
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            logger.warning(f"[TTS] Cache check error: {e}")
            return None

    def _store_cache(self, cache_key: str, audio_data: bytes):
        try:
            self.s3_client.put_object(
                Bucket=settings.S3_BUCKET,
                Key=cache_key,
                Body=audio_data,
                ContentType="audio/mpeg",
                StorageClass="INTELLIGENT_TIERING",
            )
            logger.info(f"[TTS] Cached audio: {cache_key}")
        except Exception as e:
            logger.warning(f"[TTS] Failed to cache audio: {e}")

    def synthesize(self, text: str, language: str = "hi") -> bytes:
        """Synthesize text to speech. Returns MP3 audio bytes."""
        if not self.polly_client:
            raise RuntimeError("Polly client not initialized")

        lang_key = language.lower()
        cache_key = self._cache_key(text, lang_key)

        # Check S3 cache first
        cached = self._check_cache(cache_key)
        if cached:
            return cached

        voice_id, engine, language_code = self.VOICE_CONFIG.get(lang_key, self.DEFAULT_VOICE)

        try:
            response = self.polly_client.synthesize_speech(
                Text=text[:3000],  # Polly limit per request
                OutputFormat="mp3",
                VoiceId=voice_id,
                Engine=engine,
                LanguageCode=language_code,
            )

            audio_data = response["AudioStream"].read()

            # Cache in S3 for subsequent reads
            self._store_cache(cache_key, audio_data)

            logger.info(f"[TTS] Synthesized {len(text)} chars with {voice_id} ({engine}, {language_code})")
            return audio_data

        except ClientError as e:
            logger.error(f"[TTS] Polly error: {e}")
            raise

    def is_available(self) -> bool:
        return self.polly_client is not None


tts_service = TTSService()
