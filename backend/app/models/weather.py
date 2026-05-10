from sqlalchemy import Column, Float, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy import Uuid as UUID
from datetime import datetime
from app.models.base import BaseModel

class WeatherData(BaseModel):
    __tablename__ = "weather_data"

    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    rainfall = Column(Float, nullable=False)  # mm
    wind_speed = Column(Float, nullable=False) # km/h or m/s
    pressure = Column(Float, nullable=False)   # hPa
    weather_condition = Column(String(100), nullable=True) # e.g., "Sunny", "Cloudy"
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    farm = relationship("Farm", back_populates="weather_data")

    # Composite index for efficient time-series queries per farm
    __table_args__ = (
        Index('idx_weather_farm_recorded', 'farm_id', 'recorded_at'),
    )
