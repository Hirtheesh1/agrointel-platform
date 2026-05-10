import pandas as pd
import numpy as np

class TemporalFeatureEngineer:
    """
    Engineers temporal and cyclic features for time-series forecasting.
    """
    
    def __init__(self, time_col: str = 'recorded_at'):
        self.time_col = time_col
        
    def add_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds basic time-derived features.
        """
        if self.time_col not in df.columns:
            return df
            
        df = df.copy()
        dt = pd.to_datetime(df[self.time_col])
        
        # Basic temporal features
        df['hour_of_day'] = dt.dt.hour
        df['day_of_week'] = dt.dt.dayofweek
        df['day_of_month'] = dt.dt.day
        df['month_of_year'] = dt.dt.month
        
        return df
        
    def add_cyclic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms temporal features into cyclic continuous variables using sine/cosine.
        This helps models like TFT understand that hour 23 is next to hour 0.
        """
        df = df.copy()
        
        # Ensure we have the base features
        if 'hour_of_day' not in df.columns:
            df = self.add_time_features(df)
            
        # Hours: 24 hours cycle
        df['hour_sin'] = np.sin(2 * np.pi * df['hour_of_day'] / 24.0)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour_of_day'] / 24.0)
        
        # Days of week: 7 days cycle
        df['day_week_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7.0)
        df['day_week_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7.0)
        
        # Months: 12 months cycle
        df['month_sin'] = np.sin(2 * np.pi * df['month_of_year'] / 12.0)
        df['month_cos'] = np.cos(2 * np.pi * df['month_of_year'] / 12.0)
        
        return df
        
    def add_lag_features(self, df: pd.DataFrame, columns: list, lags: list) -> pd.DataFrame:
        """
        Adds lag features (historical values) for given columns.
        """
        df = df.copy()
        for col in columns:
            if col in df.columns:
                for lag in lags:
                    df[f'{col}_lag_{lag}'] = df[col].shift(lag)
        return df
        
    def add_rolling_features(self, df: pd.DataFrame, columns: list, windows: list) -> pd.DataFrame:
        """
        Adds rolling statistics (mean, std) for specified windows.
        """
        df = df.copy()
        for col in columns:
            if col in df.columns:
                for window in windows:
                    df[f'{col}_roll_mean_{window}'] = df[col].rolling(window=window, min_periods=1).mean()
                    df[f'{col}_roll_std_{window}'] = df[col].rolling(window=window, min_periods=1).std().fillna(0)
        return df
        
    def engineer_all(self, df: pd.DataFrame, lag_cols=None, roll_cols=None) -> pd.DataFrame:
        """
        Runs the full feature engineering pipeline.
        """
        df = self.add_time_features(df)
        df = self.add_cyclic_features(df)
        
        if lag_cols:
            df = self.add_lag_features(df, lag_cols, lags=[1, 3, 6, 12, 24])
            
        if roll_cols:
            df = self.add_rolling_features(df, roll_cols, windows=[3, 6, 12, 24, 48])
            
        return df

temporal_feature_engineer = TemporalFeatureEngineer()
