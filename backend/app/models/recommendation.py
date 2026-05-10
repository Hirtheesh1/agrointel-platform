from sqlalchemy import Column, String, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from sqlalchemy import Uuid as UUID
from app.models.base import BaseModel

class Recommendation(BaseModel):
    __tablename__ = "recommendations"

    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    recommendation_type = Column(String(100), nullable=False) # e.g., "irrigation_schedule", "fertilizer_application"
    recommendation_text = Column(Text, nullable=False) # Human-readable text
    priority_level = Column(Integer, nullable=False, default=1) # 1=Low, 2=Medium, 3=High
    generated_by = Column(String(100), nullable=False) # Which part of the system generated this? (e.g., "YieldModel_v2")

    farm = relationship("Farm", back_populates="recommendations")
