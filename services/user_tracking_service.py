"""
User Tracking Service

Handles persistence of user tracking events in MongoDB.
"""

from typing import Dict
from pymongo import MongoClient
from config.settings import settings
from models.database import UserTracking


class UserTrackingService:
    """Service responsible for storing user tracking events."""

    def __init__(self):
        self.client = MongoClient(settings.mongodb_uri)
        self.collection = self.client[settings.mongodb_database][
            settings.mongodb_user_tracking_collection
        ]

    def save_event(self, payload: UserTracking) -> Dict[str, str]:
        """Persist a user tracking event."""
        document = payload.model_dump(by_alias=True, exclude_none=True)
        insert_result = self.collection.insert_one(document)
        return {"id": str(insert_result.inserted_id)}


user_tracking_service = UserTrackingService()

