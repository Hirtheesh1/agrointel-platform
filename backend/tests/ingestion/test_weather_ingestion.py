import pytest
import respx
import httpx
from datetime import datetime, timezone
from app.ingestion.weather_client import OpenWeatherClient
from app.ingestion.exceptions import APIClientError
from app.ingestion.validators import OpenWeatherRawResponse
from app.ingestion.normalizers import normalize_openweather
import uuid

@pytest.fixture
def mock_openweather_response():
    return {
        "dt": 1683648000,
        "main": {
            "temp": 35.5,
            "pressure": 1010,
            "humidity": 45
        },
        "wind": {
            "speed": 5.5
        },
        "weather": [
            {
                "main": "Clear",
                "description": "clear sky"
            }
        ]
    }

@pytest.mark.asyncio
@respx.mock
async def test_openweather_client_success(mock_openweather_response):
    """Test successful data fetch from OpenWeather."""
    client = OpenWeatherClient()
    client.api_key = "test_key"
    
    # Mock the API endpoint
    respx.get(url__startswith="https://api.openweathermap.org/data/2.5/weather").respond(
        status_code=200,
        json=mock_openweather_response
    )
    
    data = await client.fetch_current_weather(lat=11.0, lon=77.0)
    assert data["main"]["temp"] == 35.5
    assert data["weather"][0]["main"] == "Clear"

@pytest.mark.asyncio
@respx.mock
async def test_openweather_client_failure():
    """Test retry and failure handling."""
    client = OpenWeatherClient()
    client.api_key = "test_key"
    
    # Mock a 401 Unauthorized response
    respx.get(url__startswith="https://api.openweathermap.org/data/2.5/weather").respond(
        status_code=401,
        json={"message": "Invalid API key"}
    )
    
    with pytest.raises(APIClientError):
        await client.fetch_current_weather(lat=11.0, lon=77.0)

def test_normalization(mock_openweather_response):
    """Test that raw payload is properly validated and normalized."""
    farm_id = uuid.uuid4()
    
    # 1. Validation
    validated = OpenWeatherRawResponse(**mock_openweather_response)
    
    # 2. Normalization
    normalized = normalize_openweather(validated, farm_id)
    
    assert normalized.temperature == 35.5
    assert normalized.humidity == 45.0
    assert normalized.weather_condition == "Clear"
    assert normalized.rainfall == 0.0 # Default since rain wasn't in mock
