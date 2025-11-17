"""
Memory Service - Manages conversation history
Business logic for conversation memory operations
"""

from typing import List, Dict
from connectors.mongo_connector import mongo_connector
from config.settings import settings


class MemoryService:
    """Service for managing conversation memory"""

    def __init__(self):
        # Use the shared Mongo connector singleton instance to ensure we always
        # work with an object exposing the expected methods (save_message,
        # get_history, etc.) while maintaining a single MongoDB client.
        self.mongo = mongo_connector
        self.history_limit = settings.conversation_history_limit

    def save_user_message(self, session_id: str, content: str):
        """Save user message to conversation history"""
        self.mongo.save_message(session_id, "user", content)

    def save_assistant_message(self, session_id: str, content: str):
        """Save assistant message to conversation history"""
        self.mongo.save_message(session_id, "assistant", content)

    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """
        Get recent conversation history

        Returns:
            List of messages in format: [{"role": "user", "content": "..."}]
        """
        return self.mongo.get_history(session_id, limit=self.history_limit)

    def clear_conversation(self, session_id: str):
        """Delete entire conversation"""
        self.mongo.clear_session(session_id)


# Singleton instance
memory_service = MemoryService()
