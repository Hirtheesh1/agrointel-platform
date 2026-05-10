from fastapi import APIRouter
from app.api.v1.endpoints import health, weather, metrics, ai_forecast, geospatial, farm_management

api_router = APIRouter()

# Include endpoint routers here
api_router.include_router(health.router, tags=["health"])
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(ai_forecast.router, prefix="/forecast", tags=["ai-forecast"])
api_router.include_router(geospatial.router, prefix="/geospatial", tags=["geospatial"])
api_router.include_router(farm_management.router, prefix="/farm", tags=["farm-management"])
