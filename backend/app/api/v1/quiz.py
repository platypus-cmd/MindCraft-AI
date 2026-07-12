"""Quiz generation API routes."""

from fastapi import APIRouter, HTTPException, status

from app.schemas.quiz import QuizRequest, QuizResponse
from app.services import quiz_service
from app.services.gemini_errors import (
    GeminiConfigurationError,
    GeminiInvalidResponseError,
    GeminiTimeoutError,
    GeminiUpstreamError,
)

router = APIRouter(prefix="/quiz")


@router.post("/generate", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest) -> QuizResponse:
    try:
        return await quiz_service.generate_quiz(request)
    except GeminiConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Quiz generation is not configured on the server.",
        ) from exc
    except GeminiTimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Quiz generation timed out. Please try again.",
        ) from exc
    except GeminiInvalidResponseError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI response could not be validated safely.",
        ) from exc
    except GeminiUpstreamError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Quiz generation is temporarily unavailable.",
        ) from exc
