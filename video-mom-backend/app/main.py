import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
import logging
from dotenv import load_dotenv

from app.api.endpoints import router as api_router
from app.core.database import connect_to_mongo, close_mongo_connection, get_database
from app.services.file_storage import file_storage
from app.services.request_tracker import RequestTracker

load_dotenv()

logger = logging.getLogger(__name__)

# Configure CloudWatch logging if AWS credentials available
def _setup_cloudwatch_logging():
    if os.environ.get("AWS_REGION") or os.environ.get("AWS_ACCESS_KEY_ID"):
        try:
            import watchtower
            import boto3
            from app.core.config import settings
            cw_handler = watchtower.CloudWatchLogHandler(
                log_group_name=settings.CLOUDWATCH_LOG_GROUP,
                log_stream_name=f"video-mom-{os.environ.get('HOSTNAME', 'local')}",
                boto3_client=boto3.client("logs", region_name=settings.AWS_REGION),
            )
            logging.root.addHandler(cw_handler)
            logger.info("[Logger] CloudWatch logging enabled for video-mom-backend")
        except Exception as e:
            logger.warning(f"[Logger] CloudWatch not available: {e}")

_setup_cloudwatch_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    cleanup_task = asyncio.create_task(periodic_cleanup())
    
    yield
    
    # Shutdown
    cleanup_task.cancel()
    await close_mongo_connection()

async def periodic_cleanup():
    """Periodic cleanup every hour"""
    while True:
        try:
            await asyncio.sleep(3600)
            
            db = await get_database()
            tracker = RequestTracker(db)
            await tracker.cleanup_expired_requests()
            file_storage.cleanup_old_files(hours_old=24)
            
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

app = FastAPI(title="Video MOM Backend", lifespan=lifespan)

# API key validation middleware (defense-in-depth for API Gateway integration)
@app.middleware("http")
async def validate_api_key(request, call_next):
    # Skip validation for health and root endpoints
    if request.url.path in ("/", "/health", "/health/services", "/openapi.json", "/docs", "/redoc"):
        return await call_next(request)

    # Skip validation for internal Docker network requests (backend → video-mom-backend)
    client_host = request.client.host if request.client else ""
    if client_host.startswith("172.") or client_host in ("127.0.0.1", "::1", "localhost"):
        return await call_next(request)

    api_key_required = os.environ.get("API_GATEWAY_API_KEY")
    if api_key_required:
        provided_key = request.headers.get("x-api-key")
        if provided_key != api_key_required:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=403, content={"detail": "Invalid or missing API key"})

    return await call_next(request)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Video MOM Backend API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)