"""
User Tracking Controller - User tracking endpoints
"""

from fastapi import APIRouter, HTTPException, status
from models.database import UserTracking
from services.user_tracking_service import user_tracking_service

router = APIRouter()


@router.post("/user-tracking")
def user_tracking(payload: UserTracking):
    """
    User tracking endpoint

    Tracks user activity and stores in MongoDB
    """

    try:
        result = user_tracking_service.save_event(payload)
        return {"status": "success", "data": result}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store tracking event: {exc}",
        )