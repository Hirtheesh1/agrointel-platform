import os
from typing import Optional
from pytorch_forecasting import TemporalFusionTransformer

class ModelRegistry:
    """
    Manages loading and versioning of AI models.
    Future-ready for MLflow integration.
    """
    
    def __init__(self, model_dir: str = "models/"):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)
        
    def get_latest_model_path(self, model_name: str) -> Optional[str]:
        """
        Locates the most recent model checkpoint for a given name.
        """
        # A simple local registry implementation
        # Checks for files matching the model name
        candidates = [f for f in os.listdir(self.model_dir) if f.startswith(model_name) and f.endswith(".ckpt")]
        if not candidates:
            return None
            
        # Sort by modification time (latest first)
        candidates.sort(key=lambda x: os.path.getmtime(os.path.join(self.model_dir, x)), reverse=True)
        return os.path.join(self.model_dir, candidates[0])
        
    def load_model(self, model_name: str) -> Optional[TemporalFusionTransformer]:
        """
        Loads the latest TFT model.
        """
        path = self.get_latest_model_path(model_name)
        if path:
            print(f"Loading model {model_name} from {path}")
            return TemporalFusionTransformer.load_from_checkpoint(path)
        return None

    def save_model(self, model_name: str, checkpoint_path: str):
        """
        Copies a trained checkpoint to the models directory with a versioned name.
        """
        import shutil
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_path = os.path.join(self.model_dir, f"{model_name}_{timestamp}.ckpt")
        
        print(f"Registering model to {dest_path}")
        shutil.copy2(checkpoint_path, dest_path)
        return dest_path
        
model_registry = ModelRegistry()
