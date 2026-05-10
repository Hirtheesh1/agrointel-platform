import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.environment import weather as weather_repo
from app.ingestion.ingestion_service import ingestion_service
from app.processing.cleaning_service import cleaning_service
from app.processing.feature_engineering import feature_engineering_service
from app.schemas.weather import WeatherDataCreate

@pytest.mark.asyncio
async def test_end_to_end_data_pipeline(db_session: AsyncSession, sample_tamil_nadu_farm):
    """
    Test the pipeline:
    1. Fetch weather via mocked service
    2. Store in DB
    3. Retrieve from DB
    4. Clean Data
    5. Feature Engineering
    """
    # 1. Fetching logic relies on mock but let's test storage -> processing
    # Assuming ingestion has been performed, we fetch data
    db_records = await weather_repo.get_by_farm(db=db_session, farm_id=sample_tamil_nadu_farm.id, limit=100)
    
    if not db_records:
        # Insert a mock sequence if DB is empty
        for i in range(5):
            mock_in = WeatherDataCreate(
                farm_id=sample_tamil_nadu_farm.id,
                temperature=30.0 + i,
                humidity=50.0 - i,
                rainfall=0.0,
                wind_speed=5.0,
                pressure=1010.0,
                weather_condition="Clear"
            )
            await weather_repo.create(db=db_session, obj_in=mock_in)
            
        db_records = await weather_repo.get_by_farm(db=db_session, farm_id=sample_tamil_nadu_farm.id, limit=100)

    assert len(db_records) >= 5

    # 2. Convert to DataFrame (Processing Engine Input)
    import pandas as pd
    data = [
        {
            "farm_id": str(r.farm_id),
            "temperature": r.temperature,
            "humidity": r.humidity,
            "rainfall": r.rainfall,
            "wind_speed": r.wind_speed,
            "pressure": r.pressure,
            "recorded_at": r.recorded_at
        }
        for r in db_records
    ]
    df = pd.DataFrame(data)

    # 3. Clean
    cleaned_df = cleaning_service.clean_data(df)
    assert not cleaned_df.empty
    assert cleaned_df['temperature'].isna().sum() == 0

    # 4. Feature Engineering
    engineered_df = feature_engineering_service.generate_features(cleaned_df)
    
    assert "evaporation_index" in engineered_df.columns
    assert "drought_risk_score" in engineered_df.columns
    assert "humidity_trend" in engineered_df.columns
    assert "rolling_temperature_mean" in engineered_df.columns
