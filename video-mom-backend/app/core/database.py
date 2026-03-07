import os
import logging
import urllib.request
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional

logger = logging.getLogger(__name__)

class RequestStatus:
    INITIATED = "initiated"
    PROCESSING = "processing"
    RESUMED = "resumed"
    COMPLETED = "completed"
    FAILED = "failed"

class RequestType:
    TRANSCRIPTION = "transcription"
    TRANSCRIPTION_JIO = "transcription_jio"
    MOM_GENERATION = "mom_generation"
    AGENDA_GENERATION = "agenda_generation"  # Now handles issues-based generation
    AGENDA_UPDATE = "agenda_update"  # Now handles issues-based updates
    TRANSLATION = "translation"

CA_BUNDLE_URL = "https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem"
CA_BUNDLE_PATH = Path(__file__).parent.parent.parent / "certs" / "global-bundle.pem"

# MongoDB connection
mongodb_client: Optional[AsyncIOMotorClient] = None


def _is_documentdb(url: str) -> bool:
    return ".docdb.amazonaws.com" in url or os.getenv("USE_DOCUMENTDB") == "true"


def _ensure_ca_bundle() -> str:
    """Download AWS DocumentDB CA bundle if not present."""
    if CA_BUNDLE_PATH.exists():
        return str(CA_BUNDLE_PATH)

    CA_BUNDLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    logger.info("[DB] Downloading AWS DocumentDB CA bundle...")
    urllib.request.urlretrieve(CA_BUNDLE_URL, str(CA_BUNDLE_PATH))
    logger.info("[DB] CA bundle downloaded")
    return str(CA_BUNDLE_PATH)


async def connect_to_mongo():
    """Create database connection (MongoDB or DocumentDB)."""
    global mongodb_client
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

    kwargs = {}

    if _is_documentdb(mongodb_url):
        ca_path = _ensure_ca_bundle()
        kwargs["tls"] = True
        kwargs["tlsCAFile"] = ca_path
        kwargs["retryWrites"] = False
        logger.info("[DB] Connecting to Amazon DocumentDB with TLS")
    else:
        logger.info("[DB] Connecting to MongoDB")

    mongodb_client = AsyncIOMotorClient(mongodb_url, **kwargs)

async def close_mongo_connection():
    """Close database connection"""
    if mongodb_client:
        mongodb_client.close()

async def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    database_name = os.getenv("DATABASE_NAME", "eGramSabha")
    return mongodb_client[database_name]