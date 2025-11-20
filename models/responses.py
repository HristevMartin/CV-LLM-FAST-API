"""
Response models for API endpoints
These define what the API returns to the client
"""

from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""

    session_id: str = Field(..., description="Session ID")
    question: str = Field(..., description="User's original question")
    answer: str = Field(..., description="AI-generated answer")
    sources_count: int = Field(..., description="Number of CV chunks used")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "question": "What cloud platforms has Martin used?",
                "answer": "Martin has extensive experience with Google Cloud Platform...",
                "sources_count": 3
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""

    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0"
            }
        }


class SaveUserQuestionResponse(BaseModel):
    """Response model for save user question endpoint"""
    name: str = Field(..., description="Name")
    email: str = Field(..., description="Email")
    message: str = Field(..., description="Message")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "message": "What cloud platforms has Martin used?",
            }
        }