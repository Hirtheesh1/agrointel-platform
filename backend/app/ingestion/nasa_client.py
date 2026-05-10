import httpx
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.core.config import settings
from app.ingestion.exceptions import APIClientError
from app.ingestion.weather_client import BaseWeatherClient

class NasaPowerClient(BaseWeatherClient):
    """
    Concrete client for NASA POWER API (Prediction Of Worldwide Energy Resources).
    Useful for historical data and daily climatology.
    """
    def __init__(self):
        self.base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        self.timeout = httpx.Timeout(settings.HTTP_TIMEOUT_SECONDS)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
        reraise=True
    )
    async def fetch_current_weather(self, lat: float, lon: float) -> dict:
        """
        NASA POWER is daily, so we fetch data for the previous day or recent days.
        """
        # Fetching data for the last 2 days
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=2)
        
        params = {
            "parameters": "T2M,RH2M,PRECTOTCORR,WS2M",
            "community": "AG",
            "longitude": lon,
            "latitude": lat,
            "start": start_date.strftime("%Y%m%d"),
            "end": end_date.strftime("%Y%m%d"),
            "format": "JSON"
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise APIClientError(f"NASA POWER HTTP error: {e.response.status_code} - {e.response.text}") from e
        except httpx.RequestError as e:
            raise APIClientError(f"NASA POWER request failed: {str(e)}") from e
