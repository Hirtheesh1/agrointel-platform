import pytest
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.farm import farm as farm_repo
from app.repositories.environment import weather as weather_repo
from app.schemas.farm import FarmCreate
from app.schemas.weather import WeatherDataCreate
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_create_and_read_farm(db_session: AsyncSession):
    """Validates the Farm repository CRUD operations."""
    farm_in = FarmCreate(
        farm_name="Trichy Experimental Farm",
        latitude=10.7905,
        longitude=78.7047,
        farm_size=10.0
    )
    
    # Test Create
    new_farm = await farm_repo.create(db=db_session, obj_in=farm_in)
    assert new_farm.id is not None
    assert new_farm.farm_name == "Trichy Experimental Farm"
    assert new_farm.farm_size == 10.0
    
    # Test Read
    fetched_farm = await farm_repo.get(db=db_session, id=new_farm.id)
    assert fetched_farm is not None
    assert fetched_farm.id == new_farm.id

@pytest.mark.asyncio
async def test_weather_data_relationship(db_session: AsyncSession, sample_tamil_nadu_farm):
    """Validates that WeatherData correctly relates to a Farm."""
    weather_in = WeatherDataCreate(
        farm_id=sample_tamil_nadu_farm.id,
        temperature=32.5,
        humidity=65.0,
        rainfall=0.0,
        wind_speed=12.5,
        pressure=1012.0,
        weather_condition="Sunny",
        recorded_at=datetime.now(timezone.utc)
    )
    
    # Test Create
    new_weather = await weather_repo.create(db=db_session, obj_in=weather_in)
    assert new_weather.id is not None
    assert new_weather.farm_id == sample_tamil_nadu_farm.id
    
    # Test Read Multiple
    weather_records = await weather_repo.get_multi(db=db_session)
    assert len(weather_records) > 0
    assert weather_records[0].temperature == 32.5
