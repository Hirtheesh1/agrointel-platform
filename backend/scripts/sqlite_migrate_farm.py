"""
Direct SQLite migration using stdlib sqlite3 (no dependencies needed).
Run with: python scripts/sqlite_migrate_farm.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "local_pipeline.db")

MIGRATIONS = [
    "ALTER TABLE farms ADD COLUMN irrigation_method VARCHAR(50) DEFAULT 'drip'",
    "ALTER TABLE farms ADD COLUMN water_availability FLOAT DEFAULT 50.0",
    "ALTER TABLE farms ADD COLUMN active_crop VARCHAR(100)",
    "ALTER TABLE crop_profiles ADD COLUMN season VARCHAR(50)",
    "ALTER TABLE crop_profiles ADD COLUMN expected_yield_tons FLOAT",
    "ALTER TABLE crop_profiles ADD COLUMN ai_recommendation_score FLOAT",
    "ALTER TABLE crop_profiles ADD COLUMN recommendation_reasoning TEXT",
]

def apply_migrations():
    print(f"Connecting to: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for sql in MIGRATIONS:
        try:
            cursor.execute(sql)
            conn.commit()
            print(f"[OK]   {sql[:70]}...")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"[SKIP] Already exists: {sql[len('ALTER TABLE farms ADD COLUMN '):].split()[0]}")
            else:
                print(f"[ERR]  {sql[:70]} -> {e}")

    conn.close()
    print("\nMigration complete.")

if __name__ == "__main__":
    apply_migrations()
