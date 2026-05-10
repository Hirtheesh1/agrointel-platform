import torch
from pytorch_forecasting.metrics import SMAPE, MAE, RMSE, QuantileLoss
from pytorch_forecasting import TemporalFusionTransformer

class EvaluationEngine:
    """
    Evaluates forecasting model performance across multiple metrics.
    """
    
    def __init__(self, model: TemporalFusionTransformer):
        self.model = model
        self.smape = SMAPE()
        self.mae = MAE()
        self.rmse = RMSE()
        self.quantile_loss = QuantileLoss()
        
    def evaluate(self, val_dataloader) -> dict:
        """
        Runs evaluation on a validation dataloader and returns standard metrics.
        """
        self.model.eval()
        
        # We need actuals and predictions
        predictions = self.model.predict(val_dataloader, mode="prediction", return_x=False)
        actuals = torch.cat([y[0] for x, y in iter(val_dataloader)])
        
        # Calculate point metrics (using median/point forecast)
        smape_val = float(self.smape(predictions, actuals).mean())
        mae_val = float(self.mae(predictions, actuals).mean())
        rmse_val = float(self.rmse(predictions, actuals).mean())
        
        # Note: For QuantileLoss we need the raw quantile predictions, not just point predictions
        # For simplicity in this engine, we return the point metrics
        
        return {
            "SMAPE": smape_val,
            "MAE": mae_val,
            "RMSE": rmse_val
        }
