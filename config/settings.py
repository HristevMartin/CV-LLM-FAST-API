"""
Configuration settings for the CV Chatbot API

This module centralizes all configuration, loading from environment variables.
Uses pydantic-settings for validation and type safety.
"""

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # ===== API Configuration =====
    app_name: str = "CV Chatbot API"
    app_version: str = "1.0.0"
    debug: bool = False

    # ===== OpenAI Configuration =====
    openai_api_key: str = Field(..., description="OpenAI API key")
    embedding_model: str = Field(
        default="text-embedding-3-large",
        description="OpenAI embedding model"
    )
    chat_model: str = Field(
        default="gpt-4o-mini",
        description="OpenAI chat completion model"
    )
    embedding_dimensions: int = Field(
        default=3072,
        description="Embedding vector dimensions"
    )

    # ===== Typesense Configuration =====
    typesense_host: str = Field(..., description="Typesense server host")
    typesense_port: str = Field(default="8108", description="Typesense server port")
    typesense_protocol: str = Field(default="http", description="http or https")
    typesense_api_key: str = Field(..., description="Typesense API key")
    typesense_collection: str = Field(
        default="cv_chunks",
        description="Typesense collection name"
    )

    # ===== MongoDB Configuration =====
    mongodb_uri: str = Field(..., description="MongoDB connection URI")
    mongodb_database: str = Field(
        default="cv_chatbot",
        description="MongoDB database name"
    )
    mongodb_collection: str = Field(
        default="conversations",
        description="MongoDB collection for conversations"
    )
    mongodb_user_tracking_collection: str = Field(
        default="user_tracking",
        description="MongoDB collection for user tracking events"
    )

    mongodb_user_question_collection: str = Field(
        default="user_questions",
        description="MongoDB collection for user questions"
    )

    # ===== RAG Configuration =====
    rag_top_k: int = Field(
        default=5,
        description="Number of chunks to retrieve for RAG"
    )
    rag_max_distance: float = Field(
        default=0.7,
        description="Maximum vector distance threshold (0-1, lower is more similar)"
    )
    conversation_history_limit: int = Field(
        default=10,
        description="Maximum number of messages to keep in conversation history"
    )

    # ===== CV Source =====
    cv_source: str = Field(
        default="MH_CV.pdf",
        description="CV source document name (for filtering in Typesense)"
    )

    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create a singleton instance
settings = Settings()