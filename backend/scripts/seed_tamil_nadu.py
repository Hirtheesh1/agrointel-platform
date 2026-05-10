import asyncio
import os
import sys
from datetime import datetime, timedelta, timezone
import random

# Add backend directory to Python path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Default to local SQLite database for local development without Docker
if not os.environ.get("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./local_pipeline.db"

from app.core.database import AsyncSessionLocal
from app.repositories.farm import farm as farm_repo
from app.repositories.environment import weather as weather_repo
from app.schemas.farm import FarmCreate
from app.schemas.weather import WeatherDataCreate

TAMIL_NADU_REGIONS = [
    {"name": "Coimbatore Test Farm", "lat": 11.0168, "lon": 76.9558, "size": 15.0},
    {"name": "Trichy Delta Farm", "lat": 10.7905, "lon": 78.7047, "size": 25.5},
    {"name": "Salem Arid Farm", "lat": 11.6643, "lon": 78.1460, "size": 10.0},
    {"name": "Erode Turmeric Farm", "lat": 11.3410, "lon": 77.7172, "size": 12.0},
    {"name": "Thanjavur Rice Bowl", "lat": 10.7870, "lon": 79.1378, "size": 40.0},
]

def generate_realistic_weather(base_temp, is_coastal):
    """Generates somewhat realistic weather for Tamil Nadu regions."""
    # Inland gets hotter, coastal gets more humid
    temp = base_temp + random.uniform(-2.0, 4.0)
    humidity = random.uniform(70.0, 90.0) if is_coastal else random.uniform(40.0, 65.0)
    
    # 20% chance of rain
    rainfall = random.uniform(2.0, 15.0) if random.random() > 0.8 else 0.0
    wind_speed = random.uniform(5.0, 15.0)
    
    conditions = ["Clear", "Clouds", "Haze"]
    if rainfall > 0:
        conditions.append("Rain")
        
    return {
        "temperature": round(temp, 2),
        "humidity": round(humidity, 2),
        "rainfall": round(rainfall, 2),
        "wind_speed": round(wind_speed, 2),
        "pressure": round(random.uniform(1005.0, 1015.0), 2),
        "weather_condition": random.choice(conditions)
    }

async def seed_database():
    print("Starting Tamil Nadu Seed Script...")
    async with AsyncSessionLocal() as db:
        for region in TAMIL_NADU_REGIONS:
            print(f"Creating farm: {region['name']}")
            
            # 1. Create Farm
            farm_in = FarmCreate(
                farm_name=region["name"],
                latitude=region["lat"],
                longitude=region["lon"],
                farm_size=region["size"]
            )
            created_farm = await farm_repo.create(db=db, obj_in=farm_in)
            
            is_coastal = "Thanjavur" in region["name"]
            base_temp = 32.0 if is_coastal else 35.0
            
            # 2. Generate 30 days of historical weather data (hourly)
            print(f"Generating 30 days of weather history for {region['name']}...")
            now = datetime.now(timezone.utc)
            
            # Generate 720 hours of data
            for hours_ago in range(720, -1, -1):
                record_time = now - timedelta(hours=hours_ago)
                weather_data = generate_realistic_weather(base_temp, is_coastal)
                
                weather_in = WeatherDataCreate(
                    farm_id=created_farm.id,
                    recorded_at=record_time,
                    **weather_data
                )
                await weather_repo.create(db=db, obj_in=weather_in)
                
        print("Seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_database())
