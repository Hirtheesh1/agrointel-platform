from sqlalchemy import Column, String, Float, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Farm(BaseModel):
    __tablename__ = "farms"

    farm_name = Column(String(255), nullable=False, index=True)
    location_name = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    farm_size = Column(Float, nullable=True)  # in hectares
    soil_type = Column(String(100), nullable=True)

    # Geospatial Fields
    analysis_radius = Column(Float, nullable=True, default=5.0)  # radius in km
    boundary_polygon = Column(JSON, nullable=True)  # GeoJSON representing farm boundary

    # Farm Management Fields
    irrigation_method = Column(String(50), nullable=True, default="drip")  # drip/sprinkler/flood/rainfed
    water_availability = Column(Float, nullable=True, default=50.0)  # m³/day
    active_crop = Column(String(100), nullable=True)  # Currently planted crop

    # Relationships
    weather_data = relationship("WeatherData", back_populates="farm", cascade="all, delete-orphan")
    soil_data = relationship("SoilData", back_populates="farm", cascade="all, delete-orphan")
    environmental_metrics = relationship("EnvironmentalMetrics", back_populates="farm", cascade="all, delete-orphan")
    ai_predictions = relationship("AIPrediction", back_populates="farm", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="farm", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="farm", cascade="all, delete-orphan")
    crop_profiles = relationship("CropProfile", back_populates="farm", cascade="all, delete-orphan")

