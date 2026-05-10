import pandas as pd
from typing import Dict, Any, Optional
from uuid import UUID
import torch

from app.ai_engine.model_registry import model_registry
from app.ai_engine.sequence_preprocessing import sequence_preprocessor
from app.ai_engine.temporal_feature_engineering import temporal_feature_engineer
from app.ai_engine.temporal_dataset_builder import temporal_dataset_builder
from app.ai_engine.irrigation_forecaster import IrrigationForecaster
from app.ai_engine.drought_forecaster import DroughtForecaster
from app.ai_engine.environmental_intelligence import EnvironmentalIntelligenceEngine
from app.ai_engine.explainability_engine import ExplainabilityEngine

class InferenceService:
    """
    Main entry point for API endpoints to generate predictions.
    Handles data loading, preprocessing, model inference, and explainability.
    """
    
    def __init__(self):
        # In a real app, these would be loaded once during startup
        self.model = model_registry.load_model("agrointel_tft")
        
        if self.model:
            self.irrigation_forecaster = IrrigationForecaster(self.model)
            self.drought_forecaster = DroughtForecaster(self.model)
            self.env_engine = EnvironmentalIntelligenceEngine(self.model)
            self.explainability = ExplainabilityEngine(self.model)
        else:
            self.irrigation_forecaster = None
            self.drought_forecaster = None
            self.env_engine = None
            self.explainability = None
            
    def _ensure_model_loaded(self, dataset):
        if not self.model:
            print("No pre-trained model found. Initializing a structural model for local testing.")
            from app.ai_engine.tft_forecasting_engine import TFTForecastingEngine
            self.model = TFTForecastingEngine.create_model_from_dataset(dataset)
            self.irrigation_forecaster = IrrigationForecaster(self.model)
            self.drought_forecaster = DroughtForecaster(self.model)
            self.env_engine = EnvironmentalIntelligenceEngine(self.model)
            self.explainability = ExplainabilityEngine(self.model)
            
    def _prepare_inference_data(self, historical_df: pd.DataFrame):
        """
        Prepares raw historical data into a PyTorch dataloader for prediction.
        """
        if historical_df.empty:
            raise ValueError("Historical data is empty. Cannot generate sequence.")
            
        # 1. Clean and impute
        df = sequence_preprocessor.impute_missing_values(historical_df)
        
        # 2. Add time index
        df = sequence_preprocessor.add_time_idx(df)
        
        # 3. Feature engineering
        df = temporal_feature_engineer.engineer_all(
            df, 
            lag_cols=['temperature', 'humidity', 'rainfall'],
            roll_cols=['temperature', 'evaporation_index']
        )
        
        # 4. Build Dataset (Using default params used during training)
        # Note: We must pass parameters matching exactly how the model was trained.
        dataset = temporal_dataset_builder.build_dataset(
            df,
            target_col="evaporation_index",  # Or whatever the primary target is
            group_cols=["farm_id"],
            time_varying_known_reals=["time_idx", "hour_of_day", "day_of_week", "month_of_year"],
            time_varying_unknown_reals=["temperature", "humidity", "rainfall", "wind_speed"],
            static_categoricals=["farm_id"]
        )
        
        # Create dataloader for prediction
        dataloader = dataset.to_dataloader(train=False, batch_size=1, num_workers=0)
        
        self._ensure_model_loaded(dataset)
        
        return dataloader, df
        
    def get_irrigation_forecast(self, farm_id: UUID, historical_data: pd.DataFrame) -> Dict[str, Any]:
        dataloader, df = self._prepare_inference_data(historical_data)
        
        forecast = self.irrigation_forecaster.forecast(dataloader, df)
        explanation = self.explainability.generate_explanation(dataloader)
        
        return {
            "farm_id": str(farm_id),
            "forecast": forecast,
            "explainability": explanation
        }

    def get_drought_forecast(self, farm_id: UUID, historical_data: pd.DataFrame) -> Dict[str, Any]:
        dataloader, df = self._prepare_inference_data(historical_data)
        
        forecast = self.drought_forecaster.forecast(dataloader, df)
        explanation = self.explainability.generate_explanation(dataloader)
        
        return {
            "farm_id": str(farm_id),
            "forecast": forecast,
            "explainability": explanation
        }

    def get_environmental_risk(self, farm_id: UUID, historical_data: pd.DataFrame) -> Dict[str, Any]:
        dataloader, df = self._prepare_inference_data(historical_data)
        
        analysis = self.env_engine.analyze(dataloader, df)
        explanation = self.explainability.generate_explanation(dataloader)
        
        return {
            "farm_id": str(farm_id),
            "analysis": analysis,
            "explainability": explanation
        }

inference_service = InferenceService()
