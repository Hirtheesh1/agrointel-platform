import pandas as pd
import numpy as np
from typing import List, Tuple

class SequencePreprocessor:
    """
    Handles preprocessing of multivariate time-series data for PyTorch Forecasting.
    Includes imputation, normalization, and sequence ID generation.
    """
    
    def __init__(self, target_col: str = None, group_cols: List[str] = None):
        self.target_col = target_col
        self.group_cols = group_cols or ['farm_id']
        
    def impute_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Imputes missing values using forward fill, then backward fill for any remaining.
        Ensures continuous temporal sequences without NaNs which break PyTorch models.
        """
        df = df.copy()
        
        # Sort by groups and time
        if 'recorded_at' in df.columns:
            sort_cols = self.group_cols + ['recorded_at']
            df = df.sort_values(by=sort_cols)
            
        # Groupby farm/entity to avoid bleeding data across different farms
        # Use transform to apply fillna within groups
        for col in df.columns:
            if col not in self.group_cols and col != 'recorded_at':
                if df[col].isnull().any():
                    # Forward fill then backward fill within groups
                    df[col] = df.groupby(self.group_cols)[col].ffill()
                    df[col] = df.groupby(self.group_cols)[col].bfill()
                    
                    # If still NaN (e.g., entire column is NaN for a group), fill with 0
                    df[col] = df[col].fillna(0)
                    
        return df

    def add_time_idx(self, df: pd.DataFrame, time_col: str = 'recorded_at') -> pd.DataFrame:
        """
        PyTorch Forecasting requires a continuous integer `time_idx` column.
        This generates an increasing integer index for each timestep per group.
        """
        df = df.copy()
        df = df.sort_values(by=self.group_cols + [time_col])
        
        # Create a sequential time index for the entire dataset
        # Alternatively, count within each group
        df['time_idx'] = df.groupby(self.group_cols).cumcount()
        return df
        
    def filter_short_sequences(self, df: pd.DataFrame, min_length: int) -> pd.DataFrame:
        """
        Removes groups (e.g., farms) that do not have enough historical data 
        to form a proper sequence for the encoder and decoder.
        """
        counts = df.groupby(self.group_cols).size()
        valid_groups = counts[counts >= min_length].index
        
        # Support multiple group cols
        if len(self.group_cols) == 1:
            return df[df[self.group_cols[0]].isin(valid_groups)]
        else:
            # Complex filtering for multi-index
            df_indexed = df.set_index(self.group_cols)
            return df_indexed.loc[valid_groups].reset_index()

sequence_preprocessor = SequencePreprocessor()
