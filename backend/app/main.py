from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.api.v1.router import api_router
from app.ingestion import start_scheduler as start_ingestion_scheduler, shutdown_scheduler as shutdown_ingestion_scheduler
from app.processing import start_processing_scheduler, shutdown_processing_scheduler

# Setup centralized logging
setup_logging()

def create_application() -> FastAPI:
    """
    Application factory pattern to create and configure the FastAPI instance.
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Update for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    application.include_router(api_router, prefix=settings.API_V1_STR)

    return application

app = create_application()

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting up {settings.PROJECT_NAME} in {settings.ENVIRONMENT} mode.")
    start_ingestion_scheduler()
    start_processing_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.PROJECT_NAME}.")
    shutdown_processing_scheduler()
    shutdown_ingestion_scheduler()
