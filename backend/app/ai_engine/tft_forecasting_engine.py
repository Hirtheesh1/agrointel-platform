import pytorch_lightning as pl
from pytorch_forecasting import TemporalFusionTransformer, TimeSeriesDataSet
from pytorch_forecasting.metrics import QuantileLoss
import torch

class TFTForecastingEngine:
    """
    Wrapper for the PyTorch Forecasting Temporal Fusion Transformer (TFT).
    Handles model initialization from datasets and baseline hyperparameters.
    """
    
    @staticmethod
    def create_model_from_dataset(
        training_dataset: TimeSeriesDataSet,
        learning_rate: float = 0.03,
        hidden_size: int = 16,
        attention_head_size: int = 1,
        dropout: float = 0.1,
        hidden_continuous_size: int = 8
    ) -> TemporalFusionTransformer:
        """
        Initializes a fresh TFT model calibrated to the exact features 
        and scaling parameters of the provided training dataset.
        """
        
        # We use QuantileLoss to get prediction intervals (e.g. 10%, 50%, 90%)
        # This provides confidence intervals rather than just point predictions
        tft = TemporalFusionTransformer.from_dataset(
            training_dataset,
            learning_rate=learning_rate,
            hidden_size=hidden_size,
            attention_head_size=attention_head_size,
            dropout=dropout,
            hidden_continuous_size=hidden_continuous_size,
            output_size=7,  # Quantiles: 0.02, 0.1, 0.25, 0.5, 0.75, 0.9, 0.98
            loss=QuantileLoss(),
            log_interval=10, 
            reduce_on_plateau_patience=4,
        )
        return tft
        
    @staticmethod
    def load_from_checkpoint(checkpoint_path: str) -> TemporalFusionTransformer:
        """
        Loads a pre-trained TFT model from a PyTorch Lightning checkpoint.
        """
        return TemporalFusionTransformer.load_from_checkpoint(checkpoint_path)
