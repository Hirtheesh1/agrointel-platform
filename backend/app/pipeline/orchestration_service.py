import pandas as pd
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List

from app.repositories.environment import weather as weather_repo
from app.repositories.ai import prediction as prediction_repo
from app.schemas.ai import PredictionCreate
from app.ai_engine.inference_service import inference_service

class OrchestrationService:
    """
    Coordinates the end-to-end forecasting pipeline locally.
    Fetches data -> runs AI inference -> saves predictions.
    """
    
    async def _get_historical_data(self, db: AsyncSession, farm_id: UUID) -> pd.DataFrame:
        """
        Fetches the recent weather sequence from the DB.
        """
        # Fetch 168 hours (7 days) of data
        records = await weather_repo.get_by_farm(db=db, farm_id=farm_id, limit=168)
        
        if not records or len(records) < 24:
            raise ValueError(f"Insufficient historical data for farm {farm_id}. Need at least 24 hours of sequence.")
            
        data = []
        for r in records:
            data.append({
                "farm_id": str(r.farm_id),
                "recorded_at": r.recorded_at,
                "temperature": r.temperature,
                "humidity": r.humidity,
                "rainfall": r.rainfall,
                "wind_speed": r.wind_speed,
                "pressure": r.pressure,
                # In a real pipeline, we'd calculate this via processing engine,
                # but for orchestrator logic we can mock or use a default if missing.
                "evaporation_index": 5.0 
            })
            
        # Reverse to chronological order if get_by_farm returns newest first
        df = pd.DataFrame(data)
        df = df.sort_values(by='recorded_at').reset_index(drop=True)
        return df

    async def run_pipeline_for_farm(self, db: AsyncSession, farm_id: UUID) -> Dict[str, Any]:
        """
        Executes the full forecasting workflow for a single farm.
        """
        # 1. Fetch sequence
        historical_df = await self._get_historical_data(db, farm_id)
        
        # 2. Run Irrigation Forecast
        irrigation_res = inference_service.get_irrigation_forecast(farm_id, historical_df)
        
        # 3. Run Drought Forecast
        drought_res = inference_service.get_drought_forecast(farm_id, historical_df)
        
        # 4. Prepare DB schemas
        predictions_to_save: List[PredictionCreate] = []
        
        # Extract Median Irrigation Demand for the next 24 hours
        irr_forecast = irrigation_res.get("forecast", {})
        irr_demand_list = irr_forecast.get("irrigation_demand_forecast_mm", [])
        irr_val = sum(irr_demand_list[:24]) if irr_demand_list else 0.0
        
        # Extract Drought Risk
        drought_forecast = drought_res.get("forecast", {})
        drought_val = drought_forecast.get("max_probability", 0.0)
        
        # We need a confidence score from the inference
        # In our mock, we'll assign a static confidence score, but it would normally come from the Quantile spread.
        confidence = 0.85 
        
        # Create Irrigation Prediction
        predictions_to_save.append(PredictionCreate(
            farm_id=farm_id,
            prediction_type="irrigation_demand",
            prediction_value=float(irr_val),
            confidence_score=confidence,
            model_version="tft-v1.0-local",
            explanation=irrigation_res.get("explainability", {}).get("natural_language_explanation", "")
        ))
        
        # Create Drought Prediction
        predictions_to_save.append(PredictionCreate(
            farm_id=farm_id,
            prediction_type="drought_probability",
            prediction_value=float(drought_val),
            confidence_score=confidence,
            model_version="tft-v1.0-local",
            explanation=drought_res.get("explainability", {}).get("natural_language_explanation", "")
        ))
        
        # 5. Persist to Database
        saved_predictions = []
        for p_in in predictions_to_save:
            created = await prediction_repo.create(db=db, obj_in=p_in)
            saved_predictions.append(created)
            
        return {
            "status": "success",
            "farm_id": str(farm_id),
            "generated_predictions": len(saved_predictions),
            "irrigation": irrigation_res,
            "drought": drought_res
        }

orchestration_service = OrchestrationService()
