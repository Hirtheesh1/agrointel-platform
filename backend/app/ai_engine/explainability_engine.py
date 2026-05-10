import torch
from pytorch_forecasting import TemporalFusionTransformer
import numpy as np

class ExplainabilityEngine:
    """
    Uses TFT's built-in variable importance and attention weights 
    to provide human-readable explanations.
    """
    
    def __init__(self, model: TemporalFusionTransformer):
        self.model = model
        
    def generate_explanation(self, dataloader) -> dict:
        """
        Extracts variable importance and creates a textual explanation.
        """
        self.model.eval()
        
        # Get raw predictions which include interpretation metrics
        raw_predictions = self.model.predict(dataloader, mode="raw", return_x=True)
        
        # Extract interpretation
        interpretation = self.model.interpret_output(raw_predictions.output, reduction="sum")
        
        # Get variable importance
        encoder_variables = self.model.encoder_variables
        encoder_importance = interpretation["encoder_variables"].cpu().numpy().flatten()
        
        # Sort and find top drivers
        importance_dict = dict(zip(encoder_variables, encoder_importance))
        sorted_importance = sorted(importance_dict.items(), key=lambda item: item[1], reverse=True)
        
        top_driver = sorted_importance[0][0] if sorted_importance else "unknown factors"
        second_driver = sorted_importance[1][0] if len(sorted_importance) > 1 else "other environmental factors"
        
        # Example natural language generation based on drivers
        # In a real system, we would check the recent trend of the top_driver (e.g., if temperature was rising)
        explanation_text = (
            f"The forecast is primarily driven by recent changes in {top_driver} "
            f"and heavily influenced by {second_driver} over the past observation window."
        )
        
        return {
            "top_features": {k: float(v) for k, v in sorted_importance[:5]},
            "natural_language_explanation": explanation_text
        }
