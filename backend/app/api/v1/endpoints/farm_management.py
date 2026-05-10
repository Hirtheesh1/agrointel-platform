from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.models.farm import Farm
from app.schemas.farm_management import (
    FarmRegisterRequest, FarmUpdateLocationRequest,
    FarmIntelligenceResponse, CropRecommendationItem,
    IrrigationAdviceResponse, AgriculturalTimelineResponse,
)
from app.repositories.farm import farm as farm_repo
from app.farm_management.farm_decision_engine import farm_decision_engine
from app.farm_management.crop_recommendation_engine import crop_recommendation_engine
from app.farm_management.irrigation_decision_engine import irrigation_decision_engine
from app.farm_management.agricultural_timeline_engine import agricultural_timeline_engine
from app.farm_management.seasonal_forecasting_engine import seasonal_forecasting_engine

router = APIRouter()


@router.get("/farms", summary="List all registered farms")
async def list_farms(db: AsyncSession = Depends(get_db)):
    """Returns all farms in the system."""
    result = await db.execute(select(Farm))
    farms = result.scalars().all()
    return [
        {
            "id": str(f.id),
            "farm_name": f.farm_name,
            "location_name": f.location_name,
            "latitude": f.latitude,
            "longitude": f.longitude,
            "farm_size": f.farm_size,
            "soil_type": f.soil_type,
            "irrigation_method": f.irrigation_method,
            "water_availability": f.water_availability,
            "active_crop": f.active_crop,
        }
        for f in farms
    ]


@router.post("/register", summary="Register a new farm with full profile")
async def register_farm(request: FarmRegisterRequest, db: AsyncSession = Depends(get_db)):
    """
    Creates a new farm record with geospatial and management fields.
    """
    try:
        farm_data = request.model_dump()
        new_farm = await farm_repo.create(db, obj_in=farm_data)
        return new_farm
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{farm_id}/update-location", summary="Update farm location and boundary")
async def update_farm_location(
    farm_id: UUID,
    request: FarmUpdateLocationRequest,
    db: AsyncSession = Depends(get_db),
):
    farm = await db.get(Farm, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    try:
        updated = await farm_repo.update(db, db_obj=farm, obj_in=request.model_dump(exclude_none=True))
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/analyze", summary="Run full AI farm intelligence analysis")
async def analyze_farm(farm_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Runs the complete farm decision engine and returns a comprehensive intelligence report.
    """
    try:
        result = await farm_decision_engine.generate_farm_intelligence(farm_id, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommend-crops/{farm_id}", summary="Get AI crop recommendations")
async def recommend_crops(farm_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Returns top crop recommendations scored against current farm conditions.
    """
    farm = await db.get(Farm, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    farm_conditions = {
        "farm_size": farm.farm_size or 1.0,
        "water_availability": farm.water_availability or 50.0,
        "irrigation_method": farm.irrigation_method or "drip",
        "active_crop": farm.active_crop,
        "ph_level": 6.5,  # defaults (no soil data loaded here for speed)
        "avg_temperature": 30.0,
    }

    recommendations = crop_recommendation_engine.generate_recommendations(farm_conditions)
    return {"farm_id": str(farm_id), "recommendations": recommendations}


@router.get("/irrigation-advice/{farm_id}", summary="Get AI irrigation schedule")
async def get_irrigation_advice(farm_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Returns live weather-based irrigation decisions and 7-day schedule.
    """
    farm = await db.get(Farm, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    farm_conditions = {
        "farm_size": farm.farm_size or 1.0,
        "water_availability": farm.water_availability or 50.0,
        "active_crop": farm.active_crop or "Paddy",
        "soil_moisture": 45.0,
        "crop_factor": 0.85,
    }

    try:
        advice = await irrigation_decision_engine.generate_irrigation_advice(
            farm.latitude, farm.longitude, farm_conditions
        )
        return {"farm_id": str(farm_id), **advice}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/seasonal-forecast/{farm_id}", summary="Get seasonal climate forecast")
async def get_seasonal_forecast(farm_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Returns 7d, 30d, 3m, 10m seasonal forecasts with suitability scores.
    """
    farm = await db.get(Farm, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    farm_conditions = {"avg_temperature": 30.0}
    forecast = seasonal_forecasting_engine.generate_seasonal_forecast(
        farm.latitude, farm.longitude, farm_conditions
    )
    return {"farm_id": str(farm_id), "forecast": forecast}


@router.get("/agricultural-timeline/{farm_id}", summary="Get 10-month farm activity timeline")
async def get_agricultural_timeline(
    farm_id: UUID,
    crop_name: str = "Paddy",
    total_days: int = 135,
    db: AsyncSession = Depends(get_db),
):
    """
    Returns a 10-month activity and risk calendar for the specified crop.
    """
    farm = await db.get(Farm, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    timeline = agricultural_timeline_engine.generate_timeline(
        crop_name=crop_name,
        crop_total_days=total_days,
        farm_conditions={"farm_size": farm.farm_size or 1.0},
    )
    return {"farm_id": str(farm_id), **timeline}
