from abc import ABC, abstractmethod
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.core.config import settings
from app.ingestion.exceptions import APIClientError

class BaseWeatherClient(ABC):
    """
    Abstract base class for all weather API clients.
    Ensures a standard contract for fetching weather data.
    """
    
    @abstractmethod
    async def fetch_current_weather(self, lat: float, lon: float) -> dict:
        """Fetches the current weather for a given latitude and longitude."""
        pass

class OpenWeatherClient(BaseWeatherClient):
    """
    Concrete client for OpenWeather API.
    Implements robust retries with tenacity and async HTTP requests with httpx.
    """
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.timeout = httpx.Timeout(settings.HTTP_TIMEOUT_SECONDS)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
        reraise=True
    )
    async def fetch_current_weather(self, lat: float, lon: float) -> dict:
        if not self.api_key:
            raise APIClientError("OpenWeather API key is not configured.")
            
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise APIClientError(f"OpenWeather HTTP error: {e.response.status_code} - {e.response.text}") from e
        except httpx.RequestError as e:
            raise APIClientError(f"OpenWeather request failed: {str(e)}") from e
