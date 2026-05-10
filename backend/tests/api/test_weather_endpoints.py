import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.environment import weather as weather_repo
from app.schemas.weather import WeatherDataCreate
from datetime import datetime, timezone
import uuid

@pytest.mark.asyncio
async def test_get_latest_weather_not_found(client: TestClient):
    """Test the 404 response when no weather exists for a farm."""
    random_id = uuid.uuid4()
    response = client.get(f"/api/v1/weather/latest/{random_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "No weather data found for this farm."

@pytest.mark.asyncio
async def test_get_latest_weather_success(client: TestClient, db_session: AsyncSession, sample_tamil_nadu_farm):
    """Test fetching the latest weather reading successfully."""
    # 1. Insert test data
    weather_in = WeatherDataCreate(
        farm_id=sample_tamil_nadu_farm.id,
        temperature=36.0,
        humidity=40.0,
        rainfall=0.0,
        wind_speed=8.0,
        pressure=1008.0,
        weather_condition="Clear",
        recorded_at=datetime.now(timezone.utc)
    )
    await weather_repo.create(db=db_session, obj_in=weather_in)
    
    # 2. Test the API
    response = client.get(f"/api/v1/weather/latest/{sample_tamil_nadu_farm.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["temperature"] == 36.0
    assert data["weather_condition"] == "Clear"
    assert "id" in data

@pytest.mark.asyncio
async def test_trigger_manual_ingestion(client: TestClient, sample_tamil_nadu_farm):
    """Test that the manual ingestion endpoint accepts requests."""
    # The endpoint triggers a background task and returns 202 Accepted
    response = client.post(f"/api/v1/weather/ingest?farm_id={sample_tamil_nadu_farm.id}")
    assert response.status_code == 202
    assert "triggered" in response.json()["message"]
