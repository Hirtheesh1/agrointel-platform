from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProcessedMetricsBase(BaseModel):
    """
    Validates the structure of the final processed metrics before DB insertion.
    """
    average_temperature: float
    humidity_trend: str
    rainfall_average: float
    rolling_temperature_mean: float
    evaporation_index: float
    drought_risk_score: float = Field(..., ge=0.0, le=1.0)
    drought_level: str
    drought_explanation: str
    heat_stress_score: float = Field(..., ge=0.0, le=1.0)
    moisture_deficit_index: float
    analysis_timestamp: datetime
    
    class Config:
        from_attributes = True
