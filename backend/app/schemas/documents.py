"""Pydantic schemas for PDF document text extraction."""

from pydantic import BaseModel


class DocumentExtractResponse(BaseModel):
    """Response body for POST /api/v1/documents/extract.

    extracted_text is already trimmed and validated to be compatible with
    NotesRequest.source_text (50-20,000 characters) before this response is
    constructed. The uploaded filename is intentionally not echoed back.
    """

    extracted_text: str
    character_count: int
    page_count: int
