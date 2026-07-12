"""Focused revision API routes."""

from fastapi import APIRouter, HTTPException, status

from app.schemas.revision import RevisionRequest, RevisionResponse
from app.services import revision_service
from app.services.gemini_errors import (
    GeminiConfigurationError,
    GeminiInvalidResponseError,
    GeminiTimeoutError,
    GeminiUpstreamError,
)

router = APIRouter(prefix="/revision")


@router.post("/generate", response_model=RevisionResponse)
async def generate_revision(request: RevisionRequest) -> RevisionResponse:
    try:
        return await revision_service.generate_revision(request)
    except GeminiConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Revision generation is not configured on the server.",
        ) from exc
    except GeminiTimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Revision generation timed out. Please try again.",
        ) from exc
    except GeminiInvalidResponseError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI response could not be validated safely.",
        ) from exc
    except GeminiUpstreamError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Revision generation is temporarily unavailable.",
        ) from exc

