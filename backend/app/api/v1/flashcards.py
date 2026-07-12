"""Flashcards generation API routes."""

from fastapi import APIRouter, HTTPException, status

from app.schemas.flashcards import FlashcardsRequest, FlashcardsResponse
from app.services import flashcards_service
from app.services.gemini_errors import (
    GeminiConfigurationError,
    GeminiInvalidResponseError,
    GeminiTimeoutError,
    GeminiUpstreamError,
)

router = APIRouter(prefix="/flashcards")


@router.post("/generate", response_model=FlashcardsResponse)
async def generate_flashcards(request: FlashcardsRequest) -> FlashcardsResponse:
    try:
        return await flashcards_service.generate_flashcards(request)
    except GeminiConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Flashcard generation is not configured on the server.",
        ) from exc
    except GeminiTimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Flashcard generation timed out. Please try again.",
        ) from exc
    except GeminiInvalidResponseError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI response could not be validated safely.",
        ) from exc
    except GeminiUpstreamError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Flashcard generation is temporarily unavailable.",
        ) from exc
