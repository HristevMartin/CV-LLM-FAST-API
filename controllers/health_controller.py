"""
Health Controller - Health check endpoints
"""

from fastapi import APIRouter
from models.responses import HealthResponse
from config.settings import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint

    Returns API status and version
    """
    return HealthResponse(
        status="healthy",
        version=settings.app_version
    )