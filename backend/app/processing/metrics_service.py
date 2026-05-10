from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import logger
from app.repositories.environment import environment as metrics_repo
from app.schemas.ai import EnvMetricsCreate
from app.processing.validators import ProcessedMetricsBase
from app.processing.exceptions import MetricsStorageError

class MetricsService:
    """
    Handles persisting processed analytical features to the database.
    """
    async def save_metrics(self, db: AsyncSession, farm_id: UUID, processed_data: ProcessedMetricsBase) -> None:
        """
        Saves the processed metrics into the environmental_metrics table.
        """
        logger.debug(f"Saving environmental metrics for farm {farm_id}")
        
        try:
            metrics_create = EnvMetricsCreate(
                farm_id=farm_id,
                drought_risk_score=processed_data.drought_risk_score,
                heat_stress_score=processed_data.heat_stress_score,
                evaporation_index=processed_data.evaporation_index,
                drought_explanation=processed_data.drought_explanation,
                recorded_at=processed_data.analysis_timestamp
            )
            
            await metrics_repo.create(db=db, obj_in=metrics_create)
            logger.info(f"Successfully saved metrics for farm {farm_id}")
            
        except Exception as e:
            logger.error(f"Failed to save metrics for farm {farm_id}: {str(e)}")
            raise MetricsStorageError(f"Database error while saving metrics: {str(e)}")

metrics_service = MetricsService()
