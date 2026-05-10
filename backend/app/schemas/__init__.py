from app.schemas.farm import FarmCreate, FarmUpdate, FarmResponse
from app.schemas.weather import WeatherDataCreate, WeatherDataResponse
from app.schemas.soil import SoilDataCreate, SoilDataResponse
from app.schemas.ai import (
    EnvMetricsCreate, EnvMetricsResponse,
    PredictionCreate, PredictionResponse,
    RecommendationCreate, RecommendationResponse
)
from app.schemas.operations import (
    AlertCreate, AlertUpdate, AlertResponse,
    CropProfileCreate, CropProfileUpdate, CropProfileResponse
)
