from sqlalchemy import Column, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy import Uuid as UUID
from datetime import datetime
from app.models.base import BaseModel

class SoilData(BaseModel):
    __tablename__ = "soil_data"

    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    soil_moisture = Column(Float, nullable=False) # percentage
    soil_temperature = Column(Float, nullable=False)
    nitrogen_level = Column(Float, nullable=False)
    phosphorus_level = Column(Float, nullable=False)
    potassium_level = Column(Float, nullable=False)
    ph_level = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    farm = relationship("Farm", back_populates="soil_data")

    # Composite index for efficient time-series queries
    __table_args__ = (
        Index('idx_soil_farm_recorded', 'farm_id', 'recorded_at'),
    )
