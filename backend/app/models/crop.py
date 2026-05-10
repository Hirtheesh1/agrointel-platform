from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy import Uuid as UUID
from app.models.base import BaseModel

class CropProfile(BaseModel):
    __tablename__ = "crop_profiles"

    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_name = Column(String(100), nullable=False)
    planting_date = Column(DateTime, nullable=True)
    expected_harvest_date = Column(DateTime, nullable=True)
    growth_stage = Column(String(50), nullable=True)  # Germination/Vegetative/Flowering/Harvest
    irrigation_frequency = Column(Integer, nullable=True)  # Days between irrigation

    # Farm Management Fields
    season = Column(String(50), nullable=True)  # kharif/rabi/zaid/perennial
    expected_yield_tons = Column(Float, nullable=True)  # Tons/hectare
    ai_recommendation_score = Column(Float, nullable=True)  # 0.0 - 1.0
    recommendation_reasoning = Column(Text, nullable=True)  # AI explanation text

    farm = relationship("Farm", back_populates="crop_profiles")

