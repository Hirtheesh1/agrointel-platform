from sqlalchemy import Column, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy import Uuid as UUID
from datetime import datetime
from app.models.base import BaseModel

class EnvironmentalMetrics(BaseModel):
    __tablename__ = "environmental_metrics"

    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    drought_risk_score = Column(Float, nullable=True) # 0.0 to 1.0 or similar scale
    evaporation_index = Column(Float, nullable=True)
    heat_stress_score = Column(Float, nullable=True)
    humidity_trend = Column(Float, nullable=True)
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    farm = relationship("Farm", back_populates="environmental_metrics")

    __table_args__ = (
        Index('idx_env_farm_calculated', 'farm_id', 'calculated_at'),
    )
