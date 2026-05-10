from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.core.database import get_db
from app.repositories.environment import environment as metrics_repo
from app.schemas.ai import EnvMetricsResponse
from app.models.environment import EnvironmentalMetrics
from app.processing.pipeline_manager import pipeline_manager

router = APIRouter()

@router.get("/latest/{farm_id}", response_model=EnvMetricsResponse)
async def get_latest_metrics(farm_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get the most recently processed environmental metrics for a specific farm.
    """
    result = await db.execute(
        select(EnvironmentalMetrics)
        .filter(EnvironmentalMetrics.farm_id == farm_id)
        .order_by(EnvironmentalMetrics.recorded_at.desc())
        .limit(1)
    )
    latest_metrics = result.scalars().first()
    
    if not latest_metrics:
        raise HTTPException(status_code=404, detail="No processed metrics found for this farm.")
        
    return latest_metrics

@router.get("/history/{farm_id}", response_model=List[EnvMetricsResponse])
async def get_metrics_history(
    farm_id: UUID, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """
    Get historical processed metrics for a specific farm.
    """
    result = await db.execute(
        select(EnvironmentalMetrics)
        .filter(EnvironmentalMetrics.farm_id == farm_id)
        .order_by(EnvironmentalMetrics.recorded_at.desc())
        .limit(limit)
    )
    history = result.scalars().all()
    return history

@router.get("/drought/{farm_id}")
async def get_drought_analysis(farm_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get specifically the latest drought analysis for a farm.
    """
    latest = await get_latest_metrics(farm_id, db)
    return {
        "farm_id": latest.farm_id,
        "drought_risk_score": latest.drought_risk_score,
        "drought_explanation": latest.drought_explanation,
        "analysis_timestamp": latest.recorded_at
    }

@router.get("/environmental-summary/{farm_id}")
async def get_environmental_summary(farm_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get a high-level summary of the environmental stress factors.
    """
    latest = await get_latest_metrics(farm_id, db)
    return {
        "farm_id": latest.farm_id,
        "heat_stress_score": latest.heat_stress_score,
        "evaporation_index": latest.evaporation_index,
        "analysis_timestamp": latest.recorded_at
    }

@router.post("/process", status_code=202)
async def trigger_manual_processing(
    background_tasks: BackgroundTasks,
    farm_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Manually triggers the data processing pipeline.
    If farm_id is provided, processes only that farm.
    Otherwise, triggers batch processing for all farms.
    """
    if farm_id:
        background_tasks.add_task(pipeline_manager.process_farm_data, db, farm_id)
        return {"message": f"Processing pipeline triggered for farm {farm_id} in the background."}
    else:
        background_tasks.add_task(pipeline_manager.run_batch_processing, db)
        return {"message": "Batch processing triggered for all farms in the background."}
