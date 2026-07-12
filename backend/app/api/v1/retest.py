"""Targeted retest API routes."""

from fastapi import APIRouter, HTTPException, status

from app.schemas.quiz import QuizResponse
from app.schemas.retest import RetestRequest
from app.services import retest_service
from app.services.gemini_errors import (
    GeminiConfigurationError,
    GeminiInvalidResponseError,
    GeminiTimeoutError,
    GeminiUpstreamError,
)

router = APIRouter(prefix="/quizzes")


@router.post("/retest", response_model=QuizResponse)
async def generate_retest(request: RetestRequest) -> QuizResponse:
    try:
        return await retest_service.generate_retest(request)
    except GeminiConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Retest generation is not configured on the server.",
        ) from exc
    except GeminiTimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Retest generation timed out. Please try again.",
        ) from exc
    except GeminiInvalidResponseError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI response could not be validated safely.",
        ) from exc
    except GeminiUpstreamError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Retest generation is temporarily unavailable.",
        ) from exc

