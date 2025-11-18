"""
Chat Controller - Chat endpoints
Handles HTTP requests and delegates to services
"""

from fastapi import APIRouter, HTTPException
from models.requests import ChatRequest
from models.responses import ChatResponse
from services import rag_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Main chat endpoint

    Processes user question using RAG and returns answer

    Args:
        request: ChatRequest with session_id and question

    Returns:
        ChatResponse with answer and metadata
    """
    try:
        # Delegate to service layer (business logic)
        result = rag_service.process_question(
            session_id=request.session_id,
            question=request.question
        )

        return ChatResponse(
            session_id=request.session_id,
            question=request.question,
            answer=result["answer"],
            sources_count=result["sources_count"]
        )

    except Exception as e:
        # Handle errors gracefully
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )