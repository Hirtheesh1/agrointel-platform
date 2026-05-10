import pandas as pd
import numpy as np
import torch
from pytorch_forecasting import TemporalFusionTransformer

class DroughtForecaster:
    """
    Predicts drought probability and future severity using the TFT model outputs.
    """
    
    def __init__(self, model: TemporalFusionTransformer):
        self.model = model
        
    def forecast(self, dataloader, df_raw: pd.DataFrame) -> dict:
        """
        Returns drought progression over time.
        """
        self.model.eval()
        
        # Predict on the dataloader
        predictions = self.model.predict(dataloader, mode="quantiles", return_x=False)
        quantiles = predictions[0]
        
        # Assume median prediction represents base drought index
        median_forecast = quantiles[:, 3].cpu().numpy()
        
        # Normalize the raw forecast into a probability/risk score [0, 1]
        # In a real scenario, the TFT might directly output a probability 
        # or it outputs a physical value which we normalize.
        max_expected_val = 100.0  # Dummy normalization factor
        probabilities = np.clip(median_forecast / max_expected_val, 0.0, 1.0)
        
        # Determine overall severity based on max probability in the window
        max_prob = float(probabilities.max())
        if max_prob > 0.8:
            severity = "Severe"
        elif max_prob > 0.5:
            severity = "Moderate"
        else:
            severity = "Low"
            
        progression = "Worsening" if probabilities[-1] > probabilities[0] else "Improving"
        
        return {
            "drought_probability_series": probabilities.tolist(),
            "future_severity": severity,
            "progression": progression,
            "max_probability": max_prob
        }
