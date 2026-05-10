from typing import Optional
from pydantic import Field
from uuid import UUID
from datetime import datetime
from app.schemas.core import ORMBaseSchema, IDModelMixin

# --- Environmental Metrics ---

class EnvMetricsBase(ORMBaseSchema):
    farm_id: UUID
    drought_risk_score: Optional[float] = None
    evaporation_index: Optional[float] = None
    heat_stress_score: Optional[float] = None
    humidity_trend: Optional[float] = None
    calculated_at: Optional[datetime] = None

class EnvMetricsCreate(EnvMetricsBase):
    pass

class EnvMetricsResponse(EnvMetricsBase, IDModelMixin):
    created_at: datetime

# --- AI Predictions ---

class PredictionBase(ORMBaseSchema):
    farm_id: UUID
    prediction_type: str = Field(..., max_length=100)
    prediction_value: float
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    model_version: str = Field(..., max_length=50)
    explanation: Optional[str] = None
    
    model_config = {"protected_namespaces": ()}

class PredictionCreate(PredictionBase):
    pass

class PredictionResponse(PredictionBase, IDModelMixin):
    created_at: datetime

# --- Recommendations ---

class RecommendationBase(ORMBaseSchema):
    farm_id: UUID
    recommendation_type: str = Field(..., max_length=100)
    recommendation_text: str
    priority_level: int = Field(default=1)
    generated_by: str = Field(..., max_length=100)

class RecommendationCreate(RecommendationBase):
    pass

class RecommendationResponse(RecommendationBase, IDModelMixin):
    created_at: datetime
