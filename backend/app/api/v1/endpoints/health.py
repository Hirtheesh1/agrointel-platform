from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health", response_model=dict, status_code=200)
async def health_check():
    """
    Health check endpoint to verify API is up and running.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME
    }
