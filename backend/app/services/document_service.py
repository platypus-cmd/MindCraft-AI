"""PDF text extraction service.

Isolates the PDF extraction library behind this service so the library can be
replaced without changing the API route. Processing is entirely in memory:
nothing is written to disk, nothing is persisted, and Gemini is never called.
"""

import io
import logging

from fastapi import UploadFile
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.core.config import settings
from app.core.constants import (
    NOTES_SOURCE_TEXT_MAX_CHARACTERS,
    NOTES_SOURCE_TEXT_MIN_CHARACTERS,
)
from app.schemas.documents import DocumentExtractResponse
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

logger = logging.getLogger(__name__)

PDF_SIGNATURE = b"%PDF-"


async def extract_text(file: UploadFile) -> DocumentExtractResponse:
    """Extract and validate text from an uploaded PDF.

    Reads at most max_pdf_size_bytes + 1 bytes so an oversized upload can be
    rejected without buffering an arbitrarily large file into memory.
    """
    data = await file.read(settings.max_pdf_size_bytes + 1)

    if len(data) == 0:
        logger.warning("PDF rejected: empty upload")
        raise DocumentEmptyFileError("Uploaded file is empty")

    if len(data) > settings.max_pdf_size_bytes:
        logger.warning("PDF rejected: oversized upload")
        raise DocumentTooLargeError(
            "Uploaded file exceeds the maximum allowed size"
        )

    if not data.startswith(PDF_SIGNATURE):
        logger.warning("PDF rejected: invalid PDF signature")
        raise DocumentInvalidTypeError("Uploaded content is not a valid PDF")

    page_texts, page_count = _parse_pdf(data)

    combined_text = "\n\n".join(text for text in page_texts if text)
    final_text = combined_text.strip()

    if not final_text:
        logger.warning("PDF rejected: no extractable text")
        raise DocumentNoTextError("No extractable text was found in the PDF")

    character_count = len(final_text)

    if character_count < NOTES_SOURCE_TEXT_MIN_CHARACTERS:
        logger.warning("PDF rejected: extracted text below Notes minimum")
        raise DocumentTextTooShortError(
            "Extracted text is shorter than the Notes workflow minimum"
        )

    if character_count > NOTES_SOURCE_TEXT_MAX_CHARACTERS:
        logger.warning("PDF rejected: extracted text above Notes maximum")
        raise DocumentTextTooLongError(
            "Extracted text is longer than the Notes workflow maximum"
        )

    return DocumentExtractResponse(
        extracted_text=final_text,
        character_count=character_count,
        page_count=page_count,
    )


def _parse_pdf(data: bytes) -> tuple[list[str], int]:
    """Parse a PDF, reject encryption, and extract page text.

    Expected pypdf read failures are converted to DocumentParsingError.
    Unexpected programming errors are deliberately allowed to propagate.
    """
    try:
        reader = PdfReader(io.BytesIO(data))
    except PdfReadError as exc:
        logger.warning("PDF extraction failed: malformed document")
        raise DocumentParsingError("Unable to parse PDF structure") from exc

    if reader.is_encrypted:
        logger.warning("PDF rejected: encrypted document")
        raise DocumentEncryptedError("PDF is password-protected")

    try:
        page_count = len(reader.pages)
        page_texts = [(page.extract_text() or "").strip() for page in reader.pages]
    except PdfReadError as exc:
        logger.warning("PDF extraction failed: malformed document")
        raise DocumentParsingError("Unable to extract PDF text") from exc

    return page_texts, page_count