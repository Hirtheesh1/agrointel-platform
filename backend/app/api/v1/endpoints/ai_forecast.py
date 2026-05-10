from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import pandas as pd

from app.core.database import get_db
from app.repositories.ai import prediction as prediction_repo
from app.pipeline.orchestration_service import orchestration_service
from app.schemas.ai import PredictionResponse

router = APIRouter()

@router.post("/run/{farm_id}")
async def forecast_run(farm_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Triggers the end-to-end forecasting pipeline locally.
    Fetches data, runs TFT inference, and stores predictions.
    """
    try:
        result = await orchestration_service.run_pipeline_for_farm(db, farm_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/latest/{farm_id}", response_model=list[PredictionResponse])
async def get_latest_forecast(farm_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Fetches the most recently generated predictions for a farm.
    """
    # Assuming prediction_repo has a get_multi method or similar
    # We'll just fetch recent predictions
    predictions = await prediction_repo.get_multi(db, skip=0, limit=10)
    # Filter by farm_id
    farm_predictions = [p for p in predictions if p.farm_id == farm_id]
    
    if not farm_predictions:
        raise HTTPException(status_code=404, detail="No predictions found for this farm.")
        
    return farm_predictions

@router.get("/history/{farm_id}")
async def get_forecast_history(farm_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieves the history of past AI predictions for this farm.
    """
    predictions = await prediction_repo.get_multi(db, skip=0, limit=100)
    farm_predictions = [p for p in predictions if p.farm_id == farm_id]
    return {"farm_id": farm_id, "history": farm_predictions}

@router.get("/explanation/{prediction_id}")
async def get_forecast_explanation(prediction_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieves the explainability text for a specific prediction.
    """
    prediction = await prediction_repo.get(db, id=prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found.")
        
    return {
        "prediction_id": prediction_id,
        "type": prediction.prediction_type,
        "explanation": prediction.explanation
    }
