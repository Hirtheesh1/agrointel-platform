from sqlalchemy import Column, String, ForeignKey, Text, Boolean, Integer
from sqlalchemy.orm import relationship
from sqlalchemy import Uuid as UUID
from app.models.base import BaseModel

class Alert(BaseModel):
    __tablename__ = "alerts"

    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    alert_type = Column(String(100), nullable=False) # e.g., "frost_warning", "dry_soil_critical"
    alert_message = Column(Text, nullable=False)
    severity = Column(Integer, nullable=False, default=1) # 1=Info, 2=Warning, 3=Critical
    is_resolved = Column(Boolean, nullable=False, default=False, index=True)

    farm = relationship("Farm", back_populates="alerts")
