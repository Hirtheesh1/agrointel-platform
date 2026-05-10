from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.config import settings
from app.core.logging import logger
from app.core.database import AsyncSessionLocal
from app.processing.pipeline_manager import pipeline_manager

processing_scheduler_instance = AsyncIOScheduler()

async def scheduled_processing_job():
    """
    Job that runs periodically to process data for all farms.
    """
    logger.info("Executing scheduled data processing job")
    async with AsyncSessionLocal() as db:
        await pipeline_manager.run_batch_processing(db)

def start_processing_scheduler():
    """
    Configures and starts the background processing scheduler.
    """
    interval_minutes = settings.PROCESSING_INTERVAL_MINUTES
    
    # We stagger the start so it runs shortly after ingestion
    processing_scheduler_instance.add_job(
        scheduled_processing_job,
        'interval',
        minutes=interval_minutes,
        id='data_processing_job',
        replace_existing=True
    )
    
    logger.info(f"Starting Processing Scheduler. Interval set to {interval_minutes} minutes.")
    processing_scheduler_instance.start()

def shutdown_processing_scheduler():
    """
    Gracefully shuts down the processing scheduler.
    """
    logger.info("Shutting down Processing Scheduler.")
    processing_scheduler_instance.shutdown()
