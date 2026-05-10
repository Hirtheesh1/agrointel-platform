import asyncio
import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ensure we use local database for training
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./local_pipeline.db"

from app.core.database import AsyncSessionLocal
from app.ai_engine.training.dataset_builder import dataset_builder
from app.ai_engine.training.temporal_splitter import temporal_splitter
from app.ai_engine.training.sequence_generator import sequence_generator
from app.ai_engine.training.tft_trainer import tft_trainer
from app.ai_engine.training.evaluation_pipeline import evaluation_pipeline
from app.ai_engine.model_registry import model_registry

async def run_training_pipeline():
    print("Starting Production AI Training Pipeline...")
    
    async with AsyncSessionLocal() as db:
        # 1. Fetch and Preprocess Data
        print("[Stage 1] Fetching data from DB...")
        full_df = await dataset_builder.fetch_full_training_data(db)
        if full_df.empty:
            print("Error: No data found in DB. Run seed script first.")
            return
            
        # 2. Temporal Split
        print("[Stage 2] Splitting data chronologically...")
        train_df, val_df, test_df = temporal_splitter.split_data(full_df)
        
        # 3. Build PyTorch Datasets
        print("[Stage 3] Building sequences...")
        train_ds = sequence_generator.create_dataset(train_df)
        val_ds = sequence_generator.create_dataset(val_df, is_training=False, train_dataset=train_ds)
        test_ds = sequence_generator.create_dataset(test_df, is_training=False, train_dataset=train_ds)
        
        # 4. Train Model
        print("[Stage 4] Training TFT Model...")
        best_model_path = tft_trainer.train(train_ds, val_ds)
        
        # 5. Evaluate
        print("[Stage 5] Evaluating on Test Set...")
        eval_metrics = evaluation_pipeline.evaluate(best_model_path, test_ds)
        
        # 6. Save to Registry
        print("[Stage 6] Registering production model...")
        model_registry.save_model("agrointel_tft", best_model_path)
        
        print("\nTraining Pipeline Complete!")
        print(f"Metrics: {eval_metrics}")

if __name__ == "__main__":
    asyncio.run(run_training_pipeline())
