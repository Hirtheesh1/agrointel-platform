import pandas as pd
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repositories.environment import weather as weather_repo
from app.ai_engine.sequence_preprocessing import sequence_preprocessor
from app.ai_engine.temporal_feature_engineering import temporal_feature_engineer
from app.ai_engine.temporal_dataset_builder import temporal_dataset_builder

class TrainingDatasetBuilder:
    """
    Fetches raw historical data from the database and prepares it for training.
    """
    
    async def fetch_full_training_data(self, db: AsyncSession) -> pd.DataFrame:
        """
        Fetches all historical weather and environmental metrics from DB.
        """
        # Fetch all weather records (limit high for training)
        records = await weather_repo.get_multi(db, skip=0, limit=100000)
        
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
                "evaporation_index": 5.0 # Placeholder for target metric
            })
            
        df = pd.DataFrame(data)
        if df.empty:
            return df
            
        # 1. Sort and Preprocess
        df = df.sort_values(by=['farm_id', 'recorded_at']).reset_index(drop=True)
        df = sequence_preprocessor.impute_missing_values(df)
        df = sequence_preprocessor.add_time_idx(df)
        
        # 2. Feature Engineering
        df = temporal_feature_engineer.engineer_all(
            df,
            lag_cols=['temperature', 'humidity', 'rainfall'],
            roll_cols=['temperature', 'evaporation_index']
        )
        
        # 3. Clean up NaNs created by lag/rolling features
        df = df.dropna().reset_index(drop=True)
        
        return df

dataset_builder = TrainingDatasetBuilder()
