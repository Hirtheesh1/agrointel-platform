from typing import Optional
from pydantic import Field
from uuid import UUID
from datetime import datetime
from app.schemas.core import ORMBaseSchema, IDModelMixin

class WeatherDataBase(ORMBaseSchema):
    farm_id: UUID
    temperature: float
    humidity: float
    rainfall: float
    wind_speed: float
    pressure: float
    weather_condition: Optional[str] = Field(None, max_length=100)
    recorded_at: Optional[datetime] = None # If None, defaults to utcnow in DB

class WeatherDataCreate(WeatherDataBase):
    pass

class WeatherDataResponse(WeatherDataBase, IDModelMixin):
    created_at: datetime
