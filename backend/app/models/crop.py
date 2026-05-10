from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship
from sqlalchemy import Uuid as UUID
from app.models.base import BaseModel

class CropProfile(BaseModel):
    __tablename__ = "crop_profiles"

    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_name = Column(String(100), nullable=False) # e.g., "Corn", "Soybeans"
    planting_date = Column(DateTime, nullable=True)
    expected_harvest_date = Column(DateTime, nullable=True)
    growth_stage = Column(String(50), nullable=True) # e.g., "Vegetative", "Flowering", "Harvest"
    irrigation_frequency = Column(Integer, nullable=True) # Days between irrigation

    farm = relationship("Farm", back_populates="crop_profiles")
