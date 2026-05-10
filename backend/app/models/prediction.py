from sqlalchemy import Column, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy import Uuid as UUID
from app.models.base import BaseModel

class AIPrediction(BaseModel):
    __tablename__ = "ai_predictions"

    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    prediction_type = Column(String(100), nullable=False, index=True) # e.g., "irrigation", "disease_risk", "yield"
    prediction_value = Column(Float, nullable=False) # Numeric output of the model
    confidence_score = Column(Float, nullable=False) # 0.0 to 1.0 representing model certainty
    model_version = Column(String(50), nullable=False) # e.g., "v1.2.0-rf"
    explanation = Column(Text, nullable=True) # Explainable AI (XAI) output, why this prediction?

    farm = relationship("Farm", back_populates="ai_predictions")
