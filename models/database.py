"""
Database document schemas for MongoDB
These define the structure of documents stored in MongoDB
"""

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Message(BaseModel):
    """Single message in a conversation"""

    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "What cloud platforms has Martin used?",
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class Conversation(BaseModel):
    """Conversation document stored in MongoDB"""

    session_id: str = Field(..., description="Unique session identifier")
    messages: List[Message] = Field(default_factory=list, description="List of messages")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "messages": [
                    {
                        "role": "user",
                        "content": "What cloud platforms has Martin used?",
                        "timestamp": "2024-01-15T10:30:00"
                    },
                    {
                        "role": "assistant",
                        "content": "Martin has extensive experience with GCP...",
                        "timestamp": "2024-01-15T10:30:05"
                    }
                ],
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:05"
            }
        }


class UserTracking(BaseModel):
    """User tracking document stored in MongoDB"""

    id: Optional[str] = Field(default=None, alias="_id")
    ip_address: str
    user_agent: Optional[str] = None
    visited_at: datetime = Field(default_factory=datetime.utcnow)
    session_id: Optional[str] = None  
    page: Optional[str] = None 


class SaveUserQuestion(BaseModel):
    """Save user question document stored in MongoDB"""
    id: Optional[str] = Field(default=None, alias="_id")
    name: str = Field(..., description="Name")  
    email: str = Field(..., description="Email")
    message: str = Field(..., description="Message")