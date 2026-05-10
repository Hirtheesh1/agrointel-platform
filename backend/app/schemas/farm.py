from typing import Optional
from pydantic import Field
from app.schemas.core import ORMBaseSchema, IDModelMixin, TimestampMixin

class FarmBase(ORMBaseSchema):
    farm_name: str = Field(..., max_length=255)
    location_name: Optional[str] = Field(None, max_length=255)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    farm_size: Optional[float] = None
    soil_type: Optional[str] = Field(None, max_length=100)

class FarmCreate(FarmBase):
    pass

class FarmUpdate(ORMBaseSchema):
    farm_name: Optional[str] = Field(None, max_length=255)
    location_name: Optional[str] = Field(None, max_length=255)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    farm_size: Optional[float] = None
    soil_type: Optional[str] = Field(None, max_length=100)

class FarmResponse(FarmBase, IDModelMixin, TimestampMixin):
    pass
