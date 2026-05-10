from pytorch_forecasting import TemporalFusionTransformer
from pytorch_forecasting.metrics import MAE, RMSE, SMAPE
import torch
import pandas as pd

class EvaluationPipeline:
    """
    Evaluates trained models on held-out test data.
    """
    
    def evaluate(self, model_path: str, test_ds) -> dict:
        """
        Loads the best model and runs evaluation.
        """
        print(f"Loading best model from {model_path} for evaluation...")
        best_model = TemporalFusionTransformer.load_from_checkpoint(model_path)
        
        test_dataloader = test_ds.to_dataloader(train=False, batch_size=64, num_workers=0)
        
        # Calculate Metrics
        mae = MAE()
        rmse = RMSE()
        smape = SMAPE()
        
        predictions = best_model.predict(test_dataloader, return_y=True)
        
        mae_val = mae(predictions.output, predictions.y).item()
        rmse_val = rmse(predictions.output, predictions.y).item()
        smape_val = smape(predictions.output, predictions.y).item()
        
        results = {
            "mae": mae_val,
            "rmse": rmse_val,
            "smape": smape_val,
            "status": "Evaluation Complete"
        }
        
        print(f"Final Evaluation Results: MAE={mae_val:.4f}, RMSE={rmse_val:.4f}, SMAPE={smape_val:.4f}")
        return results

evaluation_pipeline = EvaluationPipeline()
