"""
Direct migration script to add farm management fields to existing SQLite DB.
Run with: python scripts/migrate_farm_management.py
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./local_pipeline.db")

from sqlalchemy import text
from app.core.database import AsyncSessionLocal

MIGRATIONS = [
    # Farm table additions
    "ALTER TABLE farms ADD COLUMN irrigation_method VARCHAR(50) DEFAULT 'drip'",
    "ALTER TABLE farms ADD COLUMN water_availability FLOAT DEFAULT 50.0",
    "ALTER TABLE farms ADD COLUMN active_crop VARCHAR(100)",
    # CropProfile table additions
    "ALTER TABLE crop_profiles ADD COLUMN season VARCHAR(50)",
    "ALTER TABLE crop_profiles ADD COLUMN expected_yield_tons FLOAT",
    "ALTER TABLE crop_profiles ADD COLUMN ai_recommendation_score FLOAT",
    "ALTER TABLE crop_profiles ADD COLUMN recommendation_reasoning TEXT",
]

async def apply_migrations():
    async with AsyncSessionLocal() as db:
        for sql in MIGRATIONS:
            try:
                await db.execute(text(sql))
                print(f"[OK] {sql[:60]}...")
            except Exception as e:
                if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                    print(f"[SKIP] Column already exists: {sql[:60]}...")
                else:
                    print(f"[ERROR] {sql[:60]}... -> {e}")
        await db.commit()
        print("\nMigration complete.")

if __name__ == "__main__":
    asyncio.run(apply_migrations())
