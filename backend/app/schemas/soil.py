from typing import Optional
from uuid import UUID
from datetime import datetime
from app.schemas.core import ORMBaseSchema, IDModelMixin

class SoilDataBase(ORMBaseSchema):
    farm_id: UUID
    soil_moisture: float
    soil_temperature: float
    nitrogen_level: float
    phosphorus_level: float
    potassium_level: float
    ph_level: float
    recorded_at: Optional[datetime] = None

class SoilDataCreate(SoilDataBase):
    pass

class SoilDataResponse(SoilDataBase, IDModelMixin):
    created_at: datetime
