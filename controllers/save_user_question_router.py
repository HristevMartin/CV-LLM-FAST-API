"""
Save User Question Controller
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.responses import SaveUserQuestionResponse
from services.user_question_service import UserQuestionService

router = APIRouter()


@router.post("/save-user-question")
def save_user_question(payload: SaveUserQuestionResponse):
    """
    Save user question endpoint
    """

    try:
        result = UserQuestionService().save_user_question(payload)
        if result[0] == "success":
            return JSONResponse(
                status_code=200,
                content={"status": "success", "data": result[1].model_dump() if hasattr(result[1], 'model_dump') else result[1]}
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": result[1]}
            )
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Failed to save user question: {exc}"}
        )