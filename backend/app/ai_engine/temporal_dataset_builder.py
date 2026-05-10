import pandas as pd
from pytorch_forecasting import TimeSeriesDataSet
from typing import List, Tuple

class TemporalDatasetBuilder:
    """
    Constructs PyTorch Forecasting TimeSeriesDataSet from DataFrames.
    Defines encoder/decoder lengths and maps features to TFT inputs.
    """
    
    def __init__(self, max_encoder_length: int = 168, max_prediction_length: int = 24):
        # Default: look back 7 days (168h), predict next 24 hours
        self.max_encoder_length = max_encoder_length
        self.max_prediction_length = max_prediction_length
        
    def build_dataset(
        self, 
        df: pd.DataFrame, 
        target_col: str, 
        group_cols: List[str], 
        time_idx_col: str = "time_idx",
        static_reals: List[str] = None,
        time_varying_known_reals: List[str] = None,
        time_varying_unknown_reals: List[str] = None,
        static_categoricals: List[str] = None,
        time_varying_known_categoricals: List[str] = None
    ) -> TimeSeriesDataSet:
        """
        Builds the primary TimeSeriesDataSet for training/validation.
        """
        
        # Ensure target is float
        if target_col in df.columns:
            df[target_col] = df[target_col].astype(float)
            
        # Ensure categoricals are strings
        all_cats = (static_categoricals or []) + (time_varying_known_categoricals or []) + group_cols
        for cat in all_cats:
            if cat in df.columns:
                df[cat] = df[cat].astype(str)
                
        dataset = TimeSeriesDataSet(
            df,
            time_idx=time_idx_col,
            target=target_col,
            group_ids=group_cols,
            min_encoder_length=self.max_encoder_length // 2,
            max_encoder_length=self.max_encoder_length,
            min_prediction_length=1,
            max_prediction_length=self.max_prediction_length,
            static_categoricals=static_categoricals or [],
            static_reals=static_reals or [],
            time_varying_known_categoricals=time_varying_known_categoricals or [],
            time_varying_known_reals=time_varying_known_reals or [],
            time_varying_unknown_categoricals=[],
            time_varying_unknown_reals=(time_varying_unknown_reals or []) + [target_col],
            add_relative_time_idx=True,
            add_target_scales=True,
            add_encoder_length=True,
        )
        
        return dataset

temporal_dataset_builder = TemporalDatasetBuilder()
