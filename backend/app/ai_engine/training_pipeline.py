import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping, LearningRateMonitor
from pytorch_lightning.loggers import TensorBoardLogger
from app.ai_engine.tft_forecasting_engine import TFTForecastingEngine
from app.ai_engine.temporal_dataset_builder import temporal_dataset_builder

class TrainingPipeline:
    """
    Orchestrates the training of the TFT model using PyTorch Lightning.
    """
    
    def __init__(self, model_name: str = "agrointel_tft"):
        self.model_name = model_name
        self.logger = TensorBoardLogger("lightning_logs", name=self.model_name)
        
    def train(self, training_dataset, val_dataset, max_epochs: int = 30):
        """
        Executes the training loop.
        """
        
        # Create DataLoaders
        train_dataloader = training_dataset.to_dataloader(train=True, batch_size=64, num_workers=0)
        val_dataloader = val_dataset.to_dataloader(train=False, batch_size=64, num_workers=0)
        
        # Initialize model
        tft = TFTForecastingEngine.create_model_from_dataset(training_dataset)
        
        # Callbacks
        early_stop_callback = EarlyStopping(
            monitor="val_loss", min_delta=1e-4, patience=5, verbose=False, mode="min"
        )
        lr_logger = LearningRateMonitor()
        
        # Trainer
        trainer = pl.Trainer(
            max_epochs=max_epochs,
            accelerator="auto",
            devices=1,
            enable_model_summary=True,
            gradient_clip_val=0.1,
            callbacks=[lr_logger, early_stop_callback],
            logger=self.logger,
            default_root_dir="models/"
        )
        
        # Train
        print(f"Starting training for {self.model_name}...")
        trainer.fit(
            tft,
            train_dataloaders=train_dataloader,
            val_dataloaders=val_dataloader,
        )
        
        # Best model path is saved automatically by PyTorch Lightning
        print(f"Training complete. Best model path: {trainer.checkpoint_callback.best_model_path}")
        return trainer.checkpoint_callback.best_model_path
