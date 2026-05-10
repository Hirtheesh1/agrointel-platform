from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID


# ─── Request Schemas ──────────────────────────────────────────────

class FarmRegisterRequest(BaseModel):
    farm_name: str
    location_name: Optional[str] = None
    latitude: float
    longitude: float
    farm_size: Optional[float] = 1.0          # hectares
    soil_type: Optional[str] = "loamy"
    irrigation_method: Optional[str] = "drip"  # drip/sprinkler/flood/rainfed
    water_availability: Optional[float] = 50.0  # m³/day
    active_crop: Optional[str] = None
    analysis_radius: Optional[float] = 5.0

class FarmUpdateLocationRequest(BaseModel):
    latitude: float
    longitude: float
    analysis_radius: Optional[float] = 5.0
    boundary_polygon: Optional[Dict[str, Any]] = None

class FarmAnalyzeRequest(BaseModel):
    farm_id: UUID


# ─── Response Schemas ─────────────────────────────────────────────

class CropRecommendationItem(BaseModel):
    crop_key: str
    crop_name: str
    season: str
    score: float
    confidence: str
    status: str
    total_days: int
    water_need_mm_day: float
    yield_range_tons: Dict[str, float]
    reasoning: str

class IrrigationScheduleItem(BaseModel):
    date: str
    day: str
    recommendation: str
    water_mm: float
    rain_prob_pct: int

class IrrigationAdviceResponse(BaseModel):
    action: str
    decision_text: str
    rain_probability_pct: int
    temperature_c: float
    humidity_pct: float
    etc_mm_day: float
    soil_moisture_pct: float
    weekly_schedule: List[IrrigationScheduleItem]

class SeasonalHorizon(BaseModel):
    label: str
    suitability_score: int
    rainfall_index: int
    drought_risk: str
    drought_color: str
    irrigation_status: str
    irrigation_color: str
    outlook: str

class SeasonalForecastResponse(BaseModel):
    day_7: SeasonalHorizon = Field(alias="7_day")
    day_30: SeasonalHorizon = Field(alias="30_day")
    month_3: SeasonalHorizon = Field(alias="3_month")
    month_10: SeasonalHorizon = Field(alias="10_month")

    model_config = {"populate_by_name": True}

class TimelineMonth(BaseModel):
    month_index: int
    month_label: str
    season: str
    rainfall_level: str
    risk_key: str
    risk_label: str
    risk_color: str
    activities: List[str]

class TimelineMilestone(BaseModel):
    day: int
    label: str
    type: str
    date: str

class AgriculturalTimelineResponse(BaseModel):
    crop_name: str
    start_date: str
    end_date: str
    months: List[TimelineMonth]
    milestones: List[TimelineMilestone]

class YieldProjectionItem(BaseModel):
    crop_name: str
    crop_key: str
    score: float
    yield_low_tons: float
    yield_expected_tons: float
    yield_high_tons: float
    farm_size_ha: float
    risk_adjusted: bool

class FarmHealthScore(BaseModel):
    score: int
    status: str
    color: str

class FarmIntelligenceResponse(BaseModel):
    farm_id: str
    farm_name: str
    location_name: Optional[str]
    farm_size_ha: Optional[float]
    active_crop: Optional[str]
    farm_conditions: Dict[str, Any]
    health_score: FarmHealthScore
    crop_recommendations: List[CropRecommendationItem]
    irrigation_advice: IrrigationAdviceResponse
    seasonal_forecast: Dict[str, SeasonalHorizon]
    yield_projections: List[YieldProjectionItem]
    agricultural_timeline: AgriculturalTimelineResponse
