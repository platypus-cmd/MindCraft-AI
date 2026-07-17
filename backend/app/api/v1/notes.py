"""Notes generation API routes."""

from fastapi import APIRouter, HTTPException, Response, status

from app.schemas.notes import (
    NotesRequest,
    NotesResponse,
    PdfExportRequest,
)
from app.services import notes_export_service, notes_service
from app.services.gemini_errors import (
    GeminiConfigurationError,
    GeminiInvalidResponseError,
    GeminiTimeoutError,
    GeminiUpstreamError,
)

router = APIRouter(prefix="/notes")


@router.post("/generate", response_model=NotesResponse)
async def generate_notes(request: NotesRequest) -> NotesResponse:
    try:
        return await notes_service.generate_notes(request)
    except GeminiConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Notes generation is not configured on the server.",
        ) from exc
    except GeminiTimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Notes generation timed out. Please try again.",
        ) from exc
    except GeminiInvalidResponseError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI response could not be validated safely.",
        ) from exc
    except GeminiUpstreamError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Notes generation is temporarily unavailable.",
        ) from exc


@router.post("/export/pdf")
async def export_notes_pdf(request: PdfExportRequest) -> Response:
    pdf_bytes = await notes_export_service.generate_notes_pdf_playwright(
        request.html_content, request.theme_class
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="mindcraft-notes.pdf"',
        },
    )
