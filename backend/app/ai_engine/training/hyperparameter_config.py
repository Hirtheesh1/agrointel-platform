from pydantic_settings import BaseSettings
from typing import List

class HyperparameterConfig(BaseSettings):
    """
    Configuration for Temporal Fusion Transformer training.
    """
    # Dataset Parameters
    max_prediction_length: int = 24  # Forecast 24 hours ahead
    max_encoder_length: int = 168    # Use 7 days of history
    batch_size: int = 64
    
    # Model Parameters
    hidden_size: int = 32
    lstm_layers: int = 2
    dropout: float = 0.1
    output_size: int = 7  # 7 quantiles by default
    attention_head_size: int = 4
    
    # Training Parameters
    learning_rate: float = 1e-3
    max_epochs: int = 50
    patience: int = 10  # Early stopping patience
    gradient_clip_val: float = 0.1
    
    # Targets & Features
    target: str = "evaporation_index"
    group_ids: List[str] = ["farm_id"]
    
    class Config:
        env_prefix = "TFT_"

tft_config = HyperparameterConfig()
