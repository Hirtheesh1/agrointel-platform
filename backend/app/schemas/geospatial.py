from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID

class FarmRegisterRequest(BaseModel):
    farm_name: str
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    analysis_radius: Optional[float] = 5.0
    boundary_polygon: Optional[Dict[str, Any]] = None # GeoJSON

class AnalyzeRegionRequest(BaseModel):
    latitude: float
    longitude: float
    radius_km: Optional[float] = 5.0

class MicroclimateResponse(BaseModel):
    farm_id: str
    farm_name: str
    center_lat: float
    center_lon: float
    radius_km: float
    insights: Dict[str, Any]
    local_stats: Dict[str, float]
    regional_baseline: Dict[str, float]
