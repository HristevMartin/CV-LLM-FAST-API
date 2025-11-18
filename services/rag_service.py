"""
RAG Service - Main orchestrator for Retrieval-Augmented Generation
Coordinates memory, embedding, and chat completion services
"""

from typing import Dict
from pathlib import Path
from connectors.openai_connector import openai_connector
from .memory_service import memory_service
from .embedding_service import embedding_service


class RAGService:
    """Main RAG orchestration service"""

    def __init__(self):
        self.openai = openai_connector
        self.memory = memory_service
        self.embedding = embedding_service
        prompt_path = Path(__file__).resolve().parent.parent / "rag_system_prompt.txt"
        if not prompt_path.exists():
            raise FileNotFoundError(f"System prompt file not found at {prompt_path}")
        self.system_prompt_template = prompt_path.read_text(encoding="utf-8")

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

        # Step 2: query needs rewriting
        search_query = question
        if self._is_vague_query(question):
            search_query = self._rewrite_query(session_id, question)

        # Step 3: Semantic search for relevant CV chunks
        hits = self.embedding.semantic_search(search_query)

        # Step 4: Handle no results (no documents retrieved or all filtered out)
        if not hits:
            answer = (
                "I couldn’t find anything in Martin Hristev’s CV that answers this question. "
                "Try asking about my skills, experience, projects, education, or certifications."
            )
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
        system_prompt = self.system_prompt_template.replace("{{context}}", cv_context.strip())
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        messages.extend(history[:-1] if len(history) > 1 else [])

        messages.append({
            "role": "user",
            "content": question
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