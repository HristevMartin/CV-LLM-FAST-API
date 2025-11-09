"""
MongoDB client connector
Handles database connections and operations
"""

from pymongo import MongoClient
from config.settings import settings
from typing import Optional, List, Dict
from datetime import datetime


class MongoConnector:
    """MongoDB client for conversation storage"""

    def __init__(self):
        """Initialize MongoDB client"""
        self.client = MongoClient(settings.mongodb_uri)
        self.db = self.client[settings.mongodb_database]
        self.collection = self.db[settings.mongodb_collection]

    def save_message(self, session_id: str, role: str, content: str):
        """
        Save a message to conversation

        Args:
            session_id: Session identifier
            role: Message role ('user' or 'assistant')
            content: Message content
        """
        self.collection.update_one(
            {"session_id": session_id},
            {
                "$setOnInsert": {"created_at": datetime.now()},
                "$set": {"updated_at": datetime.now()},
                "$push": {
                    "messages": {
                        "role": role,
                        "content": content,
                        "timestamp": datetime.now()
                    }
                }
            },
            upsert=True
        )

    def get_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """
        Get conversation history

        Args:
            session_id: Session identifier
            limit: Maximum number of messages to return

        Returns:
            List of message dicts with 'role' and 'content'
        """
        conversation = self.collection.find_one(
            {"session_id": session_id},
            {"messages": {"$slice": -limit}}
        )

        if conversation and "messages" in conversation:
            return [
                {"role": msg["role"], "content": msg["content"]}
                for msg in conversation["messages"]
            ]
        return []

    def clear_session(self, session_id: str):
        """
        Delete a conversation

        Args:
            session_id: Session identifier
        """
        self.collection.delete_one({"session_id": session_id})

    def health_check(self) -> bool:
        """Check if MongoDB is accessible"""
        try:
            self.client.server_info()
            return True
        except Exception:
            return False


mongo_connector = MongoConnector()