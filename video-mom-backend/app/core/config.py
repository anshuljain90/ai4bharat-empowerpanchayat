from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # --- Service API Keys & Endpoints ---

    # Jio STT Service (optional — not needed if using whisper only)
    JIO_API_KEY: Optional[str] = None

    # Hugging Face Services (optional — not needed if using bedrock)
    HF_TOKEN: Optional[str] = None
    STT_MODEL_ENDPOINT: Optional[str] = None
    HUGGING_FACE_LLM_ENDPOINT: Optional[str] = None
    HF_LLM: Optional[str] = None

    # --- Database ---
    MONGODB_URL: str
    DATABASE_NAME: str

    # --- AI Provider Selection ---
    STT_PROVIDER: str = "jio"  # "jio" | "whisper"
    LLM_PROVIDER: str = "huggingface"  # "huggingface" | "bedrock"
    TRANSLATION_PROVIDER: str = "llm"  # "llm" | "aws_translate"

    # --- AWS Configuration (optional — uses IAM role on EC2 if not set) ---
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    BEDROCK_MODEL_ID: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    BEDROCK_MAX_TOKENS: int = 4096

    class Config:
        # This tells pydantic to load variables from a .env file
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Create a single, reusable instance of the settings that will be
# imported by other parts of your application.
settings = Settings()