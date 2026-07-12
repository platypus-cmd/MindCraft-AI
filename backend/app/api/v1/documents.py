"""PDF document text-extraction API routes."""

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.documents import DocumentExtractResponse
from app.services import document_service
from app.services.document_errors import (
    DocumentEmptyFileError,
    DocumentEncryptedError,
    DocumentInvalidTypeError,
    DocumentNoTextError,
    DocumentParsingError,
    DocumentTextTooLongError,
    DocumentTextTooShortError,
    DocumentTooLargeError,
)

router = APIRouter(prefix="/documents")


@router.post("/extract", response_model=DocumentExtractResponse)
async def extract_document_text(
    file: UploadFile = File(...),
) -> DocumentExtractResponse:
    try:
        return await document_service.extract_text(file)
    except DocumentEmptyFileError as exc:
        raise HTTPException(
            status_code=422,
            detail="The uploaded file is empty.",
        ) from exc
    except DocumentTooLargeError as exc:
        raise HTTPException(
            status_code=413,
            detail="The PDF exceeds the maximum allowed size of 10 MB.",
        ) from exc
    except DocumentInvalidTypeError as exc:
        raise HTTPException(
            status_code=422,
            detail="Only PDF files are supported.",
        ) from exc
    except DocumentEncryptedError as exc:
        raise HTTPException(
            status_code=422,
            detail="This PDF is password-protected and cannot be processed.",
        ) from exc
    except DocumentParsingError as exc:
        raise HTTPException(
            status_code=422,
            detail="This file could not be read as a PDF.",
        ) from exc
    except DocumentNoTextError as exc:
        raise HTTPException(
            status_code=422,
            detail="No extractable text was found in this PDF.",
        ) from exc
    except DocumentTextTooShortError as exc:
        raise HTTPException(
            status_code=422,
            detail="The PDF does not contain enough extractable text to generate notes.",
        ) from exc
    except DocumentTextTooLongError as exc:
        raise HTTPException(
            status_code=422,
            detail=(
                "The extracted PDF text exceeds the 20,000-character limit. "
                "Please use a smaller PDF or a shorter document."
            ),
        ) from exc
