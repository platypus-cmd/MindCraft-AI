"""Endpoint tests for POST /api/v1/documents/extract.

See tests/test_document_service.py for the fixture-generation strategy
(pypdf.PdfWriter-based, no new production dependency).
"""

import io
import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from app.main import app
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


def _make_valid_pdf_bytes() -> bytes:
    writer = PdfWriter()
    page = writer.add_blank_page(width=200, height=200)

    text = (
        "Photosynthesis is the process plants use to convert light energy "
        "into chemical energy stored in glucose molecules for later use."
    )
    content = f"BT /F1 12 Tf 10 100 Td ({text}) Tj ET".encode("latin-1")
    stream_obj = DecodedStreamObject()
    stream_obj.set_data(content)
    stream_ref = writer._add_object(stream_obj)
    page[NameObject("/Contents")] = stream_ref

    font = DictionaryObject()
    font[NameObject("/Type")] = NameObject("/Font")
    font[NameObject("/Subtype")] = NameObject("/Type1")
    font[NameObject("/BaseFont")] = NameObject("/Helvetica")
    font_ref = writer._add_object(font)

    font_dict = DictionaryObject()
    font_dict[NameObject("/F1")] = font_ref
    resources = DictionaryObject()
    resources[NameObject("/Font")] = font_dict
    page[NameObject("/Resources")] = resources

    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


class DocumentsEndpointSuccessTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_successful_extraction_returns_200_and_expected_shape(self):
        pdf_bytes = _make_valid_pdf_bytes()

        response = self.client.post(
            "/api/v1/documents/extract",
            files={"file": ("notes.pdf", pdf_bytes, "application/pdf")},
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("Photosynthesis", body["extracted_text"])
        self.assertEqual(body["page_count"], 1)
        self.assertEqual(body["character_count"], len(body["extracted_text"]))
        self.assertNotIn("notes.pdf", body)

    def test_missing_multipart_file_returns_422(self):
        response = self.client.post("/api/v1/documents/extract")
        self.assertEqual(response.status_code, 422)


class DocumentsEndpointErrorMappingTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def _assert_error_mapping(self, exception, expected_status_code, expected_detail):
        with patch(
            "app.api.v1.documents.document_service.extract_text",
            new=AsyncMock(side_effect=exception),
        ):
            response = self.client.post(
                "/api/v1/documents/extract",
                files={"file": ("test.pdf", b"%PDF-1.4\nirrelevant", "application/pdf")},
            )

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), {"detail": expected_detail})

    def test_empty_file_error_maps_to_422(self):
        self._assert_error_mapping(
            DocumentEmptyFileError("internal detail"),
            422,
            "The uploaded file is empty.",
        )

    def test_too_large_error_maps_to_413(self):
        self._assert_error_mapping(
            DocumentTooLargeError("internal detail"),
            413,
            "The PDF exceeds the maximum allowed size of 10 MB.",
        )

    def test_invalid_type_error_maps_to_422(self):
        self._assert_error_mapping(
            DocumentInvalidTypeError("internal detail"),
            422,
            "Only PDF files are supported.",
        )

    def test_encrypted_error_maps_to_422(self):
        self._assert_error_mapping(
            DocumentEncryptedError("internal detail"),
            422,
            "This PDF is password-protected and cannot be processed.",
        )

    def test_parsing_error_maps_to_422(self):
        self._assert_error_mapping(
            DocumentParsingError("raw pypdf internals"),
            422,
            "This file could not be read as a PDF.",
        )

    def test_no_text_error_maps_to_422(self):
        self._assert_error_mapping(
            DocumentNoTextError("internal detail"),
            422,
            "No extractable text was found in this PDF.",
        )

    def test_text_too_short_error_maps_to_422(self):
        self._assert_error_mapping(
            DocumentTextTooShortError("internal detail"),
            422,
            "The PDF does not contain enough extractable text to generate notes.",
        )

    def test_text_too_long_error_maps_to_422(self):
        self._assert_error_mapping(
            DocumentTextTooLongError("internal detail"),
            422,
            "The extracted PDF text exceeds the 20,000-character limit. "
            "Please use a smaller PDF or a shorter document.",
        )


class DocumentsEndpointDoesNotCallGeminiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_extraction_never_calls_notes_service_or_gemini_service(self):
        pdf_bytes = _make_valid_pdf_bytes()

        with (
            patch("app.services.notes_service.gemini_service") as mock_gemini_service,
            patch(
                "app.api.v1.notes.notes_service.generate_notes",
                new=AsyncMock(),
            ) as mock_generate_notes,
        ):
            response = self.client.post(
                "/api/v1/documents/extract",
                files={"file": ("notes.pdf", pdf_bytes, "application/pdf")},
            )

            self.assertEqual(response.status_code, 200)
            mock_gemini_service.generate_notes_content.assert_not_called()
            mock_generate_notes.assert_not_called()


if __name__ == "__main__":
    unittest.main()
