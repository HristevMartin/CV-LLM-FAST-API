from models.database import SaveUserQuestion
from pymongo import MongoClient
from config.settings import settings

class UserQuestionService:
    """Service for saving user questions to MongoDB"""

    def __init__(self):
        self.client = MongoClient(settings.mongodb_uri)
        self.collection = self.client[settings.mongodb_database][
                settings.mongodb_user_question_collection
        ]

    def save_user_question(self, payload: SaveUserQuestion):
        """Save user question to MongoDB"""
        try:
            self.collection.insert_one(payload.model_dump(by_alias=True, exclude_none=True))
            return ("success", payload)
        except Exception as exc:
            return ("error", f"Failed to save user question: {exc}")