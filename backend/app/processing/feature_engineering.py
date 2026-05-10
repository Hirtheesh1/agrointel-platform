import pandas as pd
from datetime import datetime
from app.core.logging import logger
from app.processing.exceptions import FeatureEngineeringError
from app.processing.evaporation_engine import calculate_evaporation_index
from app.processing.humidity_analysis import calculate_humidity_trend
from app.processing.drought_engine import calculate_drought_metrics

class FeatureEngineeringService:
    """
    Orchestrates the calculation of all engineered features.
    """
    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            raise FeatureEngineeringError("Cannot generate features on an empty dataframe.")
            
        logger.debug(f"Starting feature engineering on {len(df)} records.")
        
        try:
            # 1. Simple Aggregations
            df['average_temperature'] = df['temperature'].mean()
            df['rainfall_average'] = df['rainfall'].mean()
            
            # 2. Rolling Window Statistics (e.g., 3-hour rolling average temp)
            # Since data might have gaps, ideally we set index to datetime, but assuming sorted sequential data here.
            df['rolling_temperature_mean'] = df['temperature'].rolling(window=3, min_periods=1).mean()
            
            # 3. Domain Analytics
            df['evaporation_index'] = calculate_evaporation_index(df)
            df['humidity_trend'] = calculate_humidity_trend(df)
            
            # 4. Complex Engines (Drought)
            # This relies on evaporation_index being present
            df = calculate_drought_metrics(df)
            
            # 5. Timestamp of analysis
            df['analysis_timestamp'] = datetime.utcnow()
            
            logger.debug("Feature engineering completed successfully.")
            return df
            
        except Exception as e:
            raise FeatureEngineeringError(f"Error during feature generation: {str(e)}")

feature_engineering_service = FeatureEngineeringService()
