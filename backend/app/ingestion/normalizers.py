from datetime import datetime, timezone
from uuid import UUID
from app.schemas.weather import WeatherDataCreate
from app.ingestion.validators import OpenWeatherRawResponse, NasaPowerRawResponse
from app.ingestion.exceptions import DataNormalizationError

def normalize_openweather(raw_data: OpenWeatherRawResponse, farm_id: UUID) -> WeatherDataCreate:
    """
    Normalizes a validated OpenWeather API response into the internal WeatherDataCreate schema.
    """
    try:
        # OpenWeather temperature is usually returned in Celsius (if units=metric) or Kelvin.
        # We assume units=metric is passed in the request.
        
        # Rainfall in OpenWeather is often under the "rain" dict, e.g., {"1h": 2.5}
        rainfall = 0.0
        if raw_data.rain:
            rainfall = raw_data.rain.get("1h", 0.0)
            
        weather_condition = raw_data.weather[0].main if raw_data.weather else "Unknown"
        
        return WeatherDataCreate(
            farm_id=farm_id,
            temperature=raw_data.main.temp,
            humidity=raw_data.main.humidity,
            rainfall=rainfall,
            wind_speed=raw_data.wind.speed,
            pressure=raw_data.main.pressure,
            weather_condition=weather_condition,
            recorded_at=datetime.fromtimestamp(raw_data.dt, tz=timezone.utc)
        )
    except Exception as e:
        raise DataNormalizationError(f"Failed to normalize OpenWeather data: {str(e)}")

def normalize_nasa_power(raw_data: NasaPowerRawResponse, farm_id: UUID) -> WeatherDataCreate:
    """
    Normalizes a validated NASA POWER API response into the internal schema.
    This is a stub implementation representing how a secondary source is unified.
    """
    try:
        params = raw_data.properties.parameter
        # Example parameters depending on NASA POWER requested parameters:
        # T2M (Temp 2 meters), RH2M (Relative Humidity), PRECTOTCORR (Precipitation), WS2M (Wind Speed)
        
        # For demonstration, extracting the latest key in the dictionary
        # In a real implementation, you would parse the specific date/time key.
        latest_date_key = list(params.get("T2M", {}).keys())[-1]
        
        return WeatherDataCreate(
            farm_id=farm_id,
            temperature=float(params.get("T2M", {}).get(latest_date_key, 0.0)),
            humidity=float(params.get("RH2M", {}).get(latest_date_key, 0.0)),
            rainfall=float(params.get("PRECTOTCORR", {}).get(latest_date_key, 0.0)),
            wind_speed=float(params.get("WS2M", {}).get(latest_date_key, 0.0)),
            pressure=1013.25, # Default or extracted if available
            weather_condition="Calculated from NASA",
            recorded_at=datetime.utcnow() # Should parse the actual date from the NASA payload
        )
    except Exception as e:
        raise DataNormalizationError(f"Failed to normalize NASA POWER data: {str(e)}")
