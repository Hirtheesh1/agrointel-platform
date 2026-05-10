from typing import Optional
from pydantic import Field
from uuid import UUID
from datetime import datetime
from app.schemas.core import ORMBaseSchema, IDModelMixin, TimestampMixin

# --- Alerts ---

class AlertBase(ORMBaseSchema):
    farm_id: UUID
    alert_type: str = Field(..., max_length=100)
    alert_message: str
    severity: int = Field(default=1)
    is_resolved: bool = Field(default=False)

class AlertCreate(AlertBase):
    pass

class AlertUpdate(ORMBaseSchema):
    is_resolved: Optional[bool] = None

class AlertResponse(AlertBase, IDModelMixin, TimestampMixin):
    pass

# --- Crop Profiles ---

class CropProfileBase(ORMBaseSchema):
    farm_id: UUID
    crop_name: str = Field(..., max_length=100)
    planting_date: Optional[datetime] = None
    expected_harvest_date: Optional[datetime] = None
    growth_stage: Optional[str] = Field(None, max_length=50)
    irrigation_frequency: Optional[int] = None

class CropProfileCreate(CropProfileBase):
    pass

class CropProfileUpdate(ORMBaseSchema):
    growth_stage: Optional[str] = Field(None, max_length=50)
    irrigation_frequency: Optional[int] = None

class CropProfileResponse(CropProfileBase, IDModelMixin, TimestampMixin):
    pass
