import lightning.pytorch as pl
from lightning.pytorch.callbacks import EarlyStopping, LearningRateMonitor, ModelCheckpoint
from lightning.pytorch.loggers import TensorBoardLogger
from pytorch_forecasting import TemporalFusionTransformer, QuantileLoss
from app.ai_engine.training.hyperparameter_config import tft_config

class TFTTrainer:
    """
    Orchestrates the PyTorch Lightning training loop for the TFT model.
    """
    
    def __init__(self, experiment_name: str = "agrointel_production"):
        self.logger = TensorBoardLogger("lightning_logs", name=experiment_name)
        
    def train(self, train_ds, val_ds):
        """
        Executes the training process.
        """
        # Create DataLoaders
        train_dataloader = train_ds.to_dataloader(
            train=True, batch_size=tft_config.batch_size, num_workers=0
        )
        val_dataloader = val_ds.to_dataloader(
            train=False, batch_size=tft_config.batch_size, num_workers=0
        )
        
        # Initialize TFT from dataset
        tft = TemporalFusionTransformer.from_dataset(
            train_ds,
            learning_rate=tft_config.learning_rate,
            hidden_size=tft_config.hidden_size,
            attention_head_size=tft_config.attention_head_size,
            dropout=tft_config.dropout,
            hidden_continuous_size=tft_config.hidden_size,
            output_size=tft_config.output_size,
            loss=QuantileLoss(),
            log_interval=10,
            reduce_on_plateau_patience=4
        )
        
        # Callbacks
        early_stop_callback = EarlyStopping(
            monitor="val_loss", min_delta=1e-4, patience=tft_config.patience, verbose=True, mode="min"
        )
        checkpoint_callback = ModelCheckpoint(
            monitor="val_loss", filename="best-tft-{epoch:02d}-{val_loss:.2f}", save_top_k=3, mode="min"
        )
        lr_logger = LearningRateMonitor()
        
        # Trainer
        trainer = pl.Trainer(
            max_epochs=tft_config.max_epochs,
            accelerator="auto",
            devices=1,
            gradient_clip_val=tft_config.gradient_clip_val,
            callbacks=[lr_logger, early_stop_callback, checkpoint_callback],
            logger=self.logger,
        )
        
        print(f"Starting training for {tft_config.max_epochs} epochs...")
        trainer.fit(
            tft,
            train_dataloaders=train_dataloader,
            val_dataloaders=val_dataloader,
        )
        
        return trainer.checkpoint_callback.best_model_path

tft_trainer = TFTTrainer()
