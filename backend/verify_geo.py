import asyncio
import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import AsyncSessionLocal
from app.repositories.farm import farm as farm_repo
from app.geospatial.geo_service import geo_service

async def verify_geospatial():
    print("Testing Geospatial Engine...")
    async with AsyncSessionLocal() as db:
        farms = await farm_repo.get_multi(db)
        if not farms:
            print("No farms found.")
            return
            
        test_farm = farms[0]
        print(f"Testing for Farm: {test_farm.farm_name} ({test_farm.id})")
        
        # Test Microclimate API
        try:
            result = await geo_service.analyze_farm_microclimate(db, test_farm.id)
            print("--- Microclimate Insights ---")
            print(result['insights']['text_explanation'])
            print(f"Anomalies: {result['insights']['anomalies']}")
            print(f"Temp Delta: {result['insights']['temp_delta']}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(verify_geospatial())
