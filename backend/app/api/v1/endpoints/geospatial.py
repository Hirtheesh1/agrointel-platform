from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.schemas.geospatial import FarmRegisterRequest, AnalyzeRegionRequest, MicroclimateResponse
from app.repositories.farm import farm as farm_repo
from app.geospatial.geo_service import geo_service
from app.geospatial.spatial_aggregation import spatial_aggregation

router = APIRouter()

@router.post("/farm/register")
async def register_farm(request: FarmRegisterRequest, db: AsyncSession = Depends(get_db)):
    """
    Registers a new farm with geospatial properties (radius and boundary polygon).
    """
    try:
        farm = await farm_repo.create(db, obj_in=request.model_dump())
        return farm
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/analyze-region")
async def analyze_ad_hoc_region(request: AnalyzeRegionRequest, db: AsyncSession = Depends(get_db)):
    """
    Performs an ad-hoc environmental analysis on a coordinate + radius.
    """
    try:
        baseline = await spatial_aggregation.get_regional_baseline(
            db, request.latitude, request.longitude, request.radius_km
        )
        return {"latitude": request.latitude, "longitude": request.longitude, "radius_km": request.radius_km, "environment": baseline}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/microclimate/{farm_id}", response_model=MicroclimateResponse)
async def get_microclimate(farm_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieves the microclimate intelligence and anomalies for a specific farm.
    """
    try:
        result = await geo_service.analyze_farm_microclimate(db, farm_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/environment-summary/{farm_id}")
async def get_environment_summary(farm_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieves the raw spatial aggregation data for a farm.
    """
    try:
        farm = await farm_repo.get(db, id=farm_id)
        if not farm:
            raise HTTPException(status_code=404, detail="Farm not found")
            
        baseline = await spatial_aggregation.get_regional_baseline(
            db, farm.latitude, farm.longitude, farm.analysis_radius or 5.0
        )
        return baseline
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
