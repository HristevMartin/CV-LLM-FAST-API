"""
Request models for API endpoints
These define what the client sends to the API
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""

    session_id: str = Field(
        ...,
        description="Unique session ID for conversation tracking",
        min_length=1
    )
    question: str = Field(
        ...,
        description="User's question",
        min_length=1,
        max_length=1000
    )

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "question": "What cloud platforms has Martin used?"
            }
        }