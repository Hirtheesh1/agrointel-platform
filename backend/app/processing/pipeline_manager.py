from uuid import UUID
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import logger
from app.repositories.environment import weather as weather_repo
from app.repositories.farm import farm as farm_repo
from app.processing.cleaning_service import cleaning_service
from app.processing.feature_engineering import feature_engineering_service
from app.processing.metrics_service import metrics_service
from app.processing.validators import ProcessedMetricsBase
from pydantic import ValidationError

class ProcessingPipelineManager:
    """
    Orchestrates the entire data processing and feature engineering pipeline.
    """
    async def process_farm_data(self, db: AsyncSession, farm_id: UUID) -> None:
        """
        Executes the processing pipeline for a single farm.
        """
        logger.info(f"Starting processing pipeline for farm {farm_id}")
        
        try:
            # 1. Extract raw data (e.g., last 24 records / hours)
            # In a real distributed system, this might read from a data lake (Parquet/S3).
            # Here we query the relational DB.
            raw_weather_records = await weather_repo.get_multi(db=db, limit=24) # Assuming we need recent data
            
            # Filter for this specific farm
            # Note: get_multi is a generic method. Ideally, we add a specific filter in the repo.
            farm_weather = [w for w in raw_weather_records if w.farm_id == farm_id]
            
            if not farm_weather:
                logger.warning(f"No weather data found for farm {farm_id}. Skipping processing.")
                return
                
            # Convert ORM objects to dictionaries for Pandas
            data_dicts = [
                {
                    'id': str(w.id),
                    'farm_id': str(w.farm_id),
                    'temperature': w.temperature,
                    'humidity': w.humidity,
                    'rainfall': w.rainfall,
                    'wind_speed': w.wind_speed,
                    'pressure': w.pressure,
                    'recorded_at': w.recorded_at
                } for w in farm_weather
            ]
            
            raw_df = pd.DataFrame(data_dicts)
            
            # 2. Clean Data
            cleaned_df = cleaning_service.clean_data(raw_df)
            
            # 3. Feature Engineering
            engineered_df = feature_engineering_service.generate_features(cleaned_df)
            
            # 4. Extract latest row for metrics storage (representing current analytical state)
            latest_row = engineered_df.iloc[-1].to_dict()
            
            # 5. Validate the final output
            try:
                validated_metrics = ProcessedMetricsBase(**latest_row)
            except ValidationError as e:
                logger.error(f"Validation failed for processed metrics: {e}")
                return
                
            # 6. Load (Save to DB)
            await metrics_service.save_metrics(db=db, farm_id=farm_id, processed_data=validated_metrics)
            
            logger.info(f"Successfully completed processing pipeline for farm {farm_id}")
            
        except Exception as e:
            logger.critical(f"Pipeline failed for farm {farm_id}: {str(e)}")

    async def run_batch_processing(self, db: AsyncSession) -> None:
        """
        Runs the pipeline for all active farms.
        """
        logger.info("Starting batch data processing for all farms.")
        farms = await farm_repo.get_multi(db=db, limit=1000)
        
        for farm_instance in farms:
            await self.process_farm_data(db=db, farm_id=farm_instance.id)
            
        logger.info("Completed batch data processing for all farms.")

pipeline_manager = ProcessingPipelineManager()
