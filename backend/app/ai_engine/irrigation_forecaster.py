import pandas as pd
import torch
from pytorch_forecasting import TemporalFusionTransformer

class IrrigationForecaster:
    """
    High-level wrapper for generating irrigation demand forecasts.
    Uses the underlying TFT model to predict future evaporation and moisture loss.
    """
    
    def __init__(self, model: TemporalFusionTransformer):
        self.model = model
        
    def forecast(self, dataloader, df_raw: pd.DataFrame) -> dict:
        """
        Generates forecasting horizons and confidence intervals.
        """
        self.model.eval()
        
        # Predict on the dataloader
        predictions = self.model.predict(dataloader, mode="quantiles", return_x=False)
        
        # predictions is a tensor of shape (batch_size, prediction_length, num_quantiles)
        # We assume batch_size = 1 for a single farm inference
        quantiles = predictions[0]  # shape: (prediction_length, 7)
        
        # Extract specific quantiles (e.g., median=0.5, lower=0.1, upper=0.9)
        # Assuming output_size=7 corresponds to [0.02, 0.1, 0.25, 0.5, 0.75, 0.9, 0.98]
        # Median is index 3
        median_forecast = quantiles[:, 3].cpu().numpy()
        lower_bound = quantiles[:, 1].cpu().numpy()
        upper_bound = quantiles[:, 5].cpu().numpy()
        
        # Calculate urgency based on short-term high demand
        # E.g., if the next 24 hours require significant irrigation
        short_term_demand = median_forecast[:24].sum()
        urgency = "High" if short_term_demand > 50.0 else "Low"
        
        return {
            "irrigation_demand_forecast_mm": median_forecast.tolist(),
            "confidence_lower_mm": lower_bound.tolist(),
            "confidence_upper_mm": upper_bound.tolist(),
            "urgency": urgency,
            "prediction_horizon_hours": len(median_forecast)
        }
