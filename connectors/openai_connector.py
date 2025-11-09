"""
OpenAI client connector
Handles embeddings and chat completions
"""

from openai import OpenAI
from config.settings import settings
from typing import List, Dict


class OpenAIConnector:
    """Singleton OpenAI client for embeddings and chat"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance is ever created"""
        if cls._instance is None:
            cls._instance = super(OpenAIConnector, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize OpenAI client only once"""
        # Prevent re-initialization if instance already exists
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.client = OpenAI(api_key=settings.openai_api_key)
        self.embedding_model = settings.embedding_model
        self.chat_model = settings.chat_model
        self._initialized = True

    def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding for a single text

        Args:
            text: Text to embed

        Returns:
            Embedding vector as list of floats
        """
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.3) -> str:
        """
        Generate chat completion

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)

        Returns:
            Generated response text
        """
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content

    def health_check(self) -> bool:
        """Check if OpenAI API is accessible"""
        try:
            self.client.models.list()
            return True
        except Exception:
            return False


openai_connector = OpenAIConnector()