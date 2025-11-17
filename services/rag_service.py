"""
RAG Service - Main orchestrator for Retrieval-Augmented Generation
Coordinates memory, embedding, and chat completion services
"""

from typing import Dict
from connectors.openai_connector import openai_connector
from .memory_service import memory_service
from .embedding_service import embedding_service


class RAGService:
    """Main RAG orchestration service"""

    def __init__(self):
        self.openai = openai_connector
        self.memory = memory_service
        self.embedding = embedding_service

    def _is_vague_query(self, question: str) -> bool:
        """
        Detect if query is vague (needs context from history)

        Business logic: Check for pronouns and short questions
        """
        vague_indicators = [
            "it", "that", "this", "one", "which one",
            "them", "those", "he", "she", "they",
            "more", "else", "also", "there"
        ]

        question_lower = question.lower()
        return (
                any(indicator in question_lower for indicator in vague_indicators)
                or len(question.split()) < 5
        )

    def _rewrite_query(self, session_id: str, question: str) -> str:
        """
        Rewrite vague query using conversation history

        Args:
            session_id: Session identifier
            question: Vague question

        Returns:
            Rewritten, self-contained question
        """
        history = self.memory.get_conversation_history(session_id)

        if not history:
            return question

        # Build prompt for query rewriting
        messages = [
            {
                "role": "system",
                "content": """You are a query rewriting assistant. 
Rewrite vague follow-up questions into clear, standalone questions using conversation history.
Only output the rewritten question, nothing else."""
            }
        ]

        # Add conversation history (exclude current vague question)
        messages.extend(history[:-1] if len(history) > 1 else [])

        # Add rewriting request
        messages.append({
            "role": "user",
            "content": f"Rewrite this vague question into a clear, standalone question: '{question}'"
        })

        rewritten = self.openai.chat_completion(messages, temperature=0.3)
        return rewritten.strip().strip('"').strip("'")

    def process_question(self, session_id: str, question: str) -> Dict[str, any]:
        """
        Main RAG pipeline: process question and generate answer

        Args:
            session_id: Session identifier
            question: User's question

        Returns:
            Dict with answer and metadata
        """
        # Step 1: Save user message
        self.memory.save_user_message(session_id, question)

        # Step 2: Check if query needs rewriting
        search_query = question
        if self._is_vague_query(question):
            search_query = self._rewrite_query(session_id, question)

        # Step 3: Semantic search for relevant CV chunks
        hits = self.embedding.semantic_search(search_query)

        # Step 4: Handle no results
        if not hits:
            answer = "I couldn't find relevant information in the CV to answer this question."
            self.memory.save_assistant_message(session_id, answer)
            return {
                "answer": answer,
                "sources_count": 0
            }

        # Step 5: Extract context from search results
        cv_context = self.embedding.extract_context_from_hits(hits)

        # Step 6: Get conversation history for context
        history = self.memory.get_conversation_history(session_id)

        # Step 7: Build messages for chat completion
        messages = [
            {
                "role": "system",
                "content": """You are a helpful assistant answering questions about Martin Hristev's CV.

Guidelines:
- Use conversation history for context
- Answer based on the CV context provided
- Be concise and accurate
- Prefer giving a concrete answer over saying that information is not specified.
- When the user asks about total years of experience, infer a reasonable total from the CV dates and roles.
  - If the exact number is not explicitly stated, provide your best estimate in years and clearly mark it as an estimate.
  - Example style: "Martin has approximately 5-6 years of total professional experience based on the CV timeline."
- Reference previous conversation naturally when relevant."""
            }
        ]

        messages.extend(history[:-1] if len(history) > 1 else [])

        messages.append({
            "role": "user",
            "content": f"""CV Context:

{cv_context}

Question: {question}"""
        })

        # Step 8: Generate answer
        answer = self.openai.chat_completion(messages, temperature=0.3)

        # Step 9: Save assistant message
        self.memory.save_assistant_message(session_id, answer)

        return {
            "answer": answer,
            "sources_count": len(hits)
        }


# Singleton instance
rag_service = RAGService()