from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

# --- OpenWeather API Raw Models ---

class OpenWeatherMain(BaseModel):
    temp: float
    pressure: float
    humidity: float

class OpenWeatherWind(BaseModel):
    speed: float

class OpenWeatherWeatherItem(BaseModel):
    main: str
    description: str

class OpenWeatherRawResponse(BaseModel):
    """
    Validates the raw response structure expected from OpenWeather API.
    """
    dt: int # Unix timestamp
    main: OpenWeatherMain
    wind: OpenWeatherWind
    weather: List[OpenWeatherWeatherItem]
    rain: Optional[dict] = None

    @field_validator('dt')
    def validate_timestamp(cls, v):
        if v <= 0:
            raise ValueError("Timestamp must be positive.")
        return v

# --- NASA POWER API Raw Models ---

class NasaPowerProperties(BaseModel):
    parameter: dict

class NasaPowerRawResponse(BaseModel):
    """
    Validates the raw response structure expected from NASA POWER API.
    """
    properties: NasaPowerProperties
