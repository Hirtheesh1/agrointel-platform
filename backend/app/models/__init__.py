# Export all models so Base.metadata can discover them for Alembic
from app.models.base import BaseModel
from app.models.farm import Farm
from app.models.weather import WeatherData
from app.models.soil import SoilData
from app.models.environment import EnvironmentalMetrics
from app.models.prediction import AIPrediction
from app.models.recommendation import Recommendation
from app.models.alert import Alert
from app.models.crop import CropProfile

# For convenience, expose Base as well
from app.core.database import Base
