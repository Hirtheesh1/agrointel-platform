from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.core.database import get_db
from app.repositories.environment import weather as weather_repo
from app.schemas.weather import WeatherDataResponse
from app.models.weather import WeatherData
from app.ingestion.ingestion_service import ingestion_service
from app.core.logging import logger

router = APIRouter()

@router.get("/latest/{farm_id}", response_model=WeatherDataResponse)
async def get_latest_weather(farm_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get the most recent weather reading for a specific farm.
    """
    result = await db.execute(
        select(WeatherData)
        .filter(WeatherData.farm_id == farm_id)
        .order_by(WeatherData.recorded_at.desc())
        .limit(1)
    )
    latest_weather = result.scalars().first()
    
    if not latest_weather:
        raise HTTPException(status_code=404, detail="No weather data found for this farm.")
        
    return latest_weather

@router.get("/history/{farm_id}", response_model=List[WeatherDataResponse])
async def get_weather_history(
    farm_id: UUID, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """
    Get historical weather data for a specific farm.
    """
    result = await db.execute(
        select(WeatherData)
        .filter(WeatherData.farm_id == farm_id)
        .order_by(WeatherData.recorded_at.desc())
        .limit(limit)
    )
    history = result.scalars().all()
    
    return history

@router.post("/ingest", status_code=202)
async def trigger_manual_ingestion(
    background_tasks: BackgroundTasks,
    farm_id: UUID = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Manually triggers the weather ingestion process.
    If farm_id is provided, ingests only for that farm.
    Otherwise, triggers batch ingestion for all farms.
    Executes as a background task.
    """
    if farm_id:
        background_tasks.add_task(ingestion_service.ingest_for_farm, db, farm_id)
        return {"message": f"Ingestion triggered for farm {farm_id} in the background."}
    else:
        background_tasks.add_task(ingestion_service.run_all_farms_ingestion, db)
        return {"message": "Batch ingestion triggered for all farms in the background."}
