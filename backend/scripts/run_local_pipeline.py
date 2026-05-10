import asyncio
import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set SQLite database for local non-Docker pipeline test
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./local_pipeline.db"

from app.core.database import AsyncSessionLocal, engine
from app.models.base import Base
# Import all models to ensure they are registered before create_all
from app.models import farm, weather, prediction, environment, recommendation, crop, soil, alert
from scripts.seed_tamil_nadu import seed_database
from app.repositories.farm import farm as farm_repo
from app.pipeline.orchestration_service import orchestration_service

async def run_pipeline():
    print("Starting End-to-End Local AI Forecasting Pipeline")
    
    print("\n[Stage 0] Initializing Local Database Schema...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    # 1. Seed database with farms and 168 hours of weather data
    print("\n[Stage 1] Seeding Local Database...")
    await seed_database()
    
    async with AsyncSessionLocal() as db:
        # Fetch a farm to run inference on (e.g., Coimbatore)
        farms = await farm_repo.get_multi(db, skip=0, limit=1)
        if not farms:
            print("No farms found. Seeding failed.")
            return
            
        target_farm = farms[0]
        print(f"\n[Stage 2] Running Orchestrator for Farm: {target_farm.farm_name} (ID: {target_farm.id})")
        
        # 2. Trigger Orchestration Service
        try:
            result = await orchestration_service.run_pipeline_for_farm(db, target_farm.id)
            
            print("\nPipeline Execution Successful!")
            print(f"Generated Predictions: {result.get('generated_predictions')}")
            
            print("\nIrrigation Forecast:")
            irr = result.get('irrigation', {})
            print(f" - Urgency: {irr.get('forecast', {}).get('urgency')}")
            print(f" - Explanation: {irr.get('explainability', {}).get('natural_language_explanation')}")
            
            print("\nDrought Forecast:")
            drought = result.get('drought', {})
            print(f" - Severity: {drought.get('forecast', {}).get('future_severity')}")
            print(f" - Progression: {drought.get('forecast', {}).get('progression')}")
            print(f" - Max Probability: {drought.get('forecast', {}).get('max_probability'):.2f}")
            print(f" - Explanation: {drought.get('explainability', {}).get('natural_language_explanation')}")
            
        except Exception as e:
            print(f"\nPipeline failed with error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_pipeline())
