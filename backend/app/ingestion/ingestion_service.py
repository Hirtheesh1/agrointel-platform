from uuid import UUID
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import logger
from app.repositories.environment import weather as weather_repo
from app.repositories.farm import farm as farm_repo
from app.ingestion.weather_client import OpenWeatherClient
from app.ingestion.validators import OpenWeatherRawResponse
from app.ingestion.normalizers import normalize_openweather
from app.ingestion.exceptions import IngestionError, DataValidationError

class WeatherIngestionService:
    """
    Orchestrates the fetching, validation, normalization, and saving of weather data.
    """
    def __init__(self):
        self.client = OpenWeatherClient()
        
    async def ingest_for_farm(self, db: AsyncSession, farm_id: UUID) -> None:
        """
        Runs the full ingestion pipeline for a single farm.
        """
        logger.info(f"Starting weather ingestion for farm {farm_id}")
        
        # 1. Fetch farm details (need lat/lon)
        farm_instance = await farm_repo.get(db=db, id=farm_id)
        if not farm_instance:
            logger.error(f"Farm {farm_id} not found. Skipping ingestion.")
            return
            
        if farm_instance.latitude is None or farm_instance.longitude is None:
            logger.error(f"Farm {farm_id} missing coordinates. Skipping ingestion.")
            return

        try:
            # 2. Fetch raw data
            raw_payload = await self.client.fetch_current_weather(
                lat=farm_instance.latitude, 
                lon=farm_instance.longitude
            )
            
            # 3. Validate raw data
            try:
                validated_raw = OpenWeatherRawResponse(**raw_payload)
            except ValidationError as e:
                raise DataValidationError(f"Invalid payload from OpenWeather: {e}")
                
            # 4. Normalize to internal schema
            normalized_data = normalize_openweather(validated_raw, farm_id)
            
            # 5. Save to database
            await weather_repo.create(db=db, obj_in=normalized_data)
            
            logger.info(f"Successfully ingested weather data for farm {farm_id}")
            
        except IngestionError as e:
            logger.error(f"Ingestion failed for farm {farm_id}: {str(e)}")
            # In a distributed system, we might push this to a Dead Letter Queue (DLQ) or retry topic here.
        except Exception as e:
            logger.critical(f"Unexpected error during ingestion for farm {farm_id}: {str(e)}")

    async def run_all_farms_ingestion(self, db: AsyncSession) -> None:
        """
        Fetches all farms and runs ingestion for each.
        Future optimization: Process in batches using asyncio.gather.
        """
        logger.info("Starting batch ingestion for all farms")
        farms = await farm_repo.get_multi(db=db, limit=1000) # Pagination for massive scale
        
        for farm_instance in farms:
            await self.ingest_for_farm(db=db, farm_id=farm_instance.id)
            
        logger.info("Completed batch ingestion for all farms")

ingestion_service = WeatherIngestionService()
