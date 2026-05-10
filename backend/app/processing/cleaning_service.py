import pandas as pd
import numpy as np
from app.core.logging import logger
from app.processing.exceptions import DataCleaningError

class CleaningService:
    """
    Cleans raw weather data using Pandas.
    Handles missing values, duplicates, and outliers.
    """
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            raise DataCleaningError("Input dataframe is empty.")
            
        logger.debug(f"Starting data cleaning on {len(df)} records.")
        
        # 1. Sort by timestamp to ensure chronological order for time-series operations
        if 'recorded_at' in df.columns:
            df = df.sort_values('recorded_at')
            
        # 2. Remove exact duplicates based on timestamp and farm_id
        df = df.drop_duplicates(subset=['farm_id', 'recorded_at'], keep='last')
        
        # 3. Handle missing values
        # Forward fill for environmental metrics (assume continuity), then backward fill if first row is NaN
        cols_to_fill = ['temperature', 'humidity', 'wind_speed', 'pressure', 'rainfall']
        df[cols_to_fill] = df[cols_to_fill].ffill().bfill()
        
        # 4. Cap outliers (e.g., impossible temperatures or humidity > 100)
        # Humidity should be 0-100%
        df['humidity'] = np.clip(df['humidity'], 0, 100)
        
        # Temperature bounds (-50C to 60C)
        df['temperature'] = np.clip(df['temperature'], -50.0, 60.0)
        
        # Rainfall cannot be negative
        df['rainfall'] = np.clip(df['rainfall'], 0.0, None)
        
        # Wind speed cannot be negative
        df['wind_speed'] = np.clip(df['wind_speed'], 0.0, None)

        logger.debug(f"Finished data cleaning. {len(df)} records remaining.")
        return df

cleaning_service = CleaningService()
