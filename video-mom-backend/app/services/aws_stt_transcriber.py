import os
import time
import uuid
import logging
import requests
import boto3
from app.core.config import settings

logger = logging.getLogger(__name__)

# AWS Transcribe language code mapping
LANGUAGE_CODE_MAP = {
    "English": "en-US",
    "Hindi": "hi-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Bengali": "bn-IN",
    "Gujarati": "gu-IN",
    "Marathi": "mr-IN",
    "Punjabi": "pa-IN",
    "Assamese": "ab-IN",  # closest available
    "Urdu": "ur-IN",      # not natively supported, fallback
    "Spanish": "es-US",
    "French": "fr-FR",
    "German": "de-DE",
    "Italian": "it-IT",
    "Portuguese": "pt-BR",
    "Russian": "ru-RU",
    "Korean": "ko-KR",
    "Turkish": "tr-TR",
    "Vietnamese": "vi-VN",
    "Thai": "th-TH",
    "Dutch": "nl-NL",
    "Polish": "pl-PL",
    "Arabic": "ar-SA",
    "Malay": "ms-MY",
    "Tagalog": "tl-PH",
    "Bahasa": "id-ID",
}

MEDIA_FORMAT_MAP = {
    ".wav": "wav",
    ".mp3": "mp3",
    ".mp4": "mp4",
    ".m4a": "mp4",
    ".flac": "flac",
    ".ogg": "ogg",
    ".webm": "webm",
}


class AWSTranscribeSTT:
    """AWS Transcribe STT service (batch mode via S3)"""

    def __init__(self):
        self.region = settings.AWS_REGION
        self.bucket = settings.AWS_TRANSCRIBE_BUCKET

        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=self.region,
        )
        self.s3 = session.client("s3")
        self.transcribe = session.client("transcribe")

        # Ensure bucket exists
        self._ensure_bucket()
        logger.info(
            f"AWS Transcribe STT initialized (region={self.region}, bucket={self.bucket})"
        )

    def _ensure_bucket(self):
        """Create the S3 bucket if it doesn't already exist."""
        try:
            self.s3.head_bucket(Bucket=self.bucket)
        except self.s3.exceptions.ClientError:
            logger.info(f"Creating S3 bucket: {self.bucket}")
            if self.region == "us-east-1":
                self.s3.create_bucket(Bucket=self.bucket)
            else:
                self.s3.create_bucket(
                    Bucket=self.bucket,
                    CreateBucketConfiguration={"LocationConstraint": self.region},
                )

    def transcribe_audio(self, audio_file_path: str, language: str = "Hindi") -> str:
        """Transcribe an audio file using AWS Transcribe."""
        job_name = f"egram-stt-{uuid.uuid4().hex[:12]}"
        s3_key = f"transcribe-input/{job_name}/{os.path.basename(audio_file_path)}"

        try:
            # 1. Upload to S3
            logger.info(f"Uploading {audio_file_path} to s3://{self.bucket}/{s3_key}")
            self.s3.upload_file(audio_file_path, self.bucket, s3_key)

            s3_uri = f"s3://{self.bucket}/{s3_key}"
            lang_code = LANGUAGE_CODE_MAP.get(language, "hi-IN")
            media_fmt = MEDIA_FORMAT_MAP.get(
                os.path.splitext(audio_file_path)[1].lower(), "wav"
            )

            # 2. Start transcription job
            logger.info(
                f"Starting AWS Transcribe job {job_name} (lang={lang_code}, fmt={media_fmt})"
            )
            self.transcribe.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={"MediaFileUri": s3_uri},
                MediaFormat=media_fmt,
                LanguageCode=lang_code,
            )

            # 3. Poll until complete (timeout after 5 min)
            deadline = time.time() + 300
            while time.time() < deadline:
                resp = self.transcribe.get_transcription_job(
                    TranscriptionJobName=job_name
                )
                status = resp["TranscriptionJob"]["TranscriptionJobStatus"]

                if status == "COMPLETED":
                    transcript_uri = resp["TranscriptionJob"]["Transcript"][
                        "TranscriptFileUri"
                    ]
                    result = requests.get(transcript_uri, timeout=30).json()
                    transcript = result["results"]["transcripts"][0]["transcript"]
                    logger.info(
                        f"AWS Transcribe job {job_name} completed, length={len(transcript)}"
                    )
                    return transcript.strip()

                if status == "FAILED":
                    reason = resp["TranscriptionJob"].get(
                        "FailureReason", "Unknown error"
                    )
                    raise Exception(f"AWS Transcribe job failed: {reason}")

                time.sleep(3)

            raise Exception("AWS Transcribe job timed out after 5 minutes")

        except Exception as e:
            logger.error(f"AWS Transcribe error: {e}", exc_info=True)
            raise

        finally:
            # Cleanup S3 object and transcription job
            try:
                self.s3.delete_object(Bucket=self.bucket, Key=s3_key)
            except Exception:
                pass
            try:
                self.transcribe.delete_transcription_job(
                    TranscriptionJobName=job_name
                )
            except Exception:
                pass


# Global instance (lazy — only created when STT_PROVIDER=aws_transcribe)
aws_stt_transcriber = None


def get_aws_stt_transcriber() -> AWSTranscribeSTT:
    global aws_stt_transcriber
    if aws_stt_transcriber is None:
        aws_stt_transcriber = AWSTranscribeSTT()
    return aws_stt_transcriber
