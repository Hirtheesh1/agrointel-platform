from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.config import settings
from app.core.logging import logger
from app.core.database import AsyncSessionLocal
from app.ingestion.ingestion_service import ingestion_service

# Create a global instance of the scheduler
scheduler = AsyncIOScheduler()

async def scheduled_ingestion_job():
    """
    Job that runs periodically to fetch weather data for all farms.
    """
    logger.info("Executing scheduled weather ingestion job")
    async with AsyncSessionLocal() as db:
        await ingestion_service.run_all_farms_ingestion(db)

def start_scheduler():
    """
    Configures and starts the background scheduler.
    """
    interval_minutes = settings.WEATHER_POLLING_INTERVAL_MINUTES
    
    # Add the ingestion job
    scheduler.add_job(
        scheduled_ingestion_job,
        'interval',
        minutes=interval_minutes,
        id='weather_ingestion_job',
        replace_existing=True
    )
    
    logger.info(f"Starting APScheduler. Weather polling interval set to {interval_minutes} minutes.")
    scheduler.start()

def shutdown_scheduler():
    """
    Gracefully shuts down the scheduler.
    """
    logger.info("Shutting down APScheduler.")
    scheduler.shutdown()
