from app.repositories.base import CRUDBase
from app.models.prediction import AIPrediction
from app.models.recommendation import Recommendation
from app.schemas.ai import PredictionCreate, PredictionBase, RecommendationCreate, RecommendationBase

class RepositoryAIPrediction(CRUDBase[AIPrediction, PredictionCreate, PredictionBase]):
    pass

class RepositoryRecommendation(CRUDBase[Recommendation, RecommendationCreate, RecommendationBase]):
    pass

prediction = RepositoryAIPrediction(AIPrediction)
recommendation = RepositoryRecommendation(Recommendation)
