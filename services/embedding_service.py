"""
Embedding Service - Handles embeddings and vector search
Business logic for semantic search operations
"""

from typing import List, Dict
from connectors.openai_connector import openai_connector
from connectors.typesense_connector import  typesense_connector
from config.settings import settings


class EmbeddingService:
    """Service for embedding generation and semantic search"""

    def __init__(self):
        self.openai = openai_connector
        self.typesense = typesense_connector
        self.max_distance = settings.rag_max_distance
        self.top_k = settings.rag_top_k
        self.cv_source = settings.cv_source

    def  semantic_search(self, question: str, k: int = None) -> List[Dict]:
        """
        Perform semantic search on CV chunks

        Args:
            question: User's question
            k: Number of results (defaults to settings.rag_top_k)

        Returns:
            List of relevant CV chunks with metadata
        """
        k = k or self.top_k

        # Step 1: Create embedding for the question
        query_vector = self.openai.create_embedding(question)

        # Step 2: Search in Typesense
        hits = self.typesense.vector_search(
            query_vector=query_vector,
            k=k,
            source_filter=self.cv_source
        )

        # Step 3: Filter by distance threshold (business logic)
        relevant_hits = [
            hit for hit in hits
            if hit.get('vector_distance', 1.0) <= self.max_distance
        ]

        return relevant_hits

    def extract_context_from_hits(self, hits: List[Dict]) -> str:
        """
        Extract and format context from search hits

        Args:
            hits: Search results from Typesense

        Returns:
            Formatted context string for RAG
        """
        if not hits:
            return ""

        context_parts = []
        for hit in hits:
            doc = hit.get('document', {})
            section = doc.get('section', 'unknown')
            text = doc.get('text', '')
            context_parts.append(f"[{section}]: {text}")

        return "\n\n".join(context_parts)


# Singleton instance
embedding_service = EmbeddingService()