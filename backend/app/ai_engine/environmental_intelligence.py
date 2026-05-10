import pandas as pd
import numpy as np
import torch
from pytorch_forecasting import TemporalFusionTransformer

class EnvironmentalIntelligenceEngine:
    """
    Analyzes climate anomalies and environmental instability.
    """
    
    def __init__(self, model: TemporalFusionTransformer):
        self.model = model
        
    def analyze(self, dataloader, df_raw: pd.DataFrame) -> dict:
        """
        Calculates heat stress evolution and environmental instability.
        """
        self.model.eval()
        
        # Predict on the dataloader
        predictions = self.model.predict(dataloader, mode="quantiles", return_x=False)
        quantiles = predictions[0]
        
        # Median forecast
        median_forecast = quantiles[:, 3].cpu().numpy()
        
        # Volatility / Instability calculation (using the variance/spread of the forecast)
        # Upper bound (90th percentile) - Lower bound (10th percentile)
        upper_bound = quantiles[:, 5].cpu().numpy()
        lower_bound = quantiles[:, 1].cpu().numpy()
        
        spread = upper_bound - lower_bound
        avg_spread = float(np.mean(spread))
        
        instability_index = avg_spread / 100.0  # Normalized relative to expected domain scale
        
        # Heat stress evolution (mocked based on forecast slope)
        trend = float(np.polyfit(np.arange(len(median_forecast)), median_forecast, 1)[0])
        
        if trend > 0.5:
            heat_stress = "Rapidly Increasing"
        elif trend > 0.1:
            heat_stress = "Gradually Increasing"
        elif trend > -0.1:
            heat_stress = "Stable"
        else:
            heat_stress = "Decreasing"
            
        anomalies_detected = bool(np.any(spread > (avg_spread * 2.0)))
        
        return {
            "environmental_instability_index": instability_index,
            "heat_stress_evolution": heat_stress,
            "climate_anomalies_detected": anomalies_detected,
            "trend_slope": trend
        }
