import pandas as pd
from typing import Tuple

from app.ai_engine.training.hyperparameter_config import tft_config

class TemporalSplitter:
    """
    Handles chronological splitting of multi-series datasets to prevent data leakage.
    """
    
    @staticmethod
    def split_data(
        df: pd.DataFrame, 
        train_ratio: float = 0.8, 
        val_ratio: float = 0.1
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Splits data chronologically across all groups.
        """
        if df.empty:
            return df, df, df
            
        # Ensure time index exists
        if 'time_idx' not in df.columns:
            raise ValueError("Dataframe must have 'time_idx' for temporal splitting.")
            
        max_time = df['time_idx'].max()
        train_cutoff = int(max_time * train_ratio)
        val_cutoff = int(max_time * (train_ratio + val_ratio))
        
        # Validation and Test sets need historical overlap to build their first sequence
        overlap = tft_config.max_encoder_length
        
        train_df = df[df['time_idx'] <= train_cutoff]
        val_df = df[(df['time_idx'] > train_cutoff - overlap) & (df['time_idx'] <= val_cutoff)]
        test_df = df[df['time_idx'] > val_cutoff - overlap]
        
        return train_df, val_df, test_df

temporal_splitter = TemporalSplitter()
