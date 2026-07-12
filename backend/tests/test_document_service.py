"""Tests for app.services.document_service.

Test-fixture strategy:
No new production dependency is added merely to generate test PDFs.
pypdf is already a production dependency of this project (used for the
extraction itself), so these fixtures are built with pypdf.PdfWriter,
constructing each page's /Contents stream and /Resources font dictionary
directly (pypdf's PdfWriter has no built-in "write text" helper, so the
minimal content-stream operators are written by hand). This keeps fixture
generation deterministic, in-memory, and dependency-free beyond what the
service already requires. `PdfWriter._add_object` is a private pypdf API;
it is used here only in test code, not in production code, and is
acceptable for that narrow purpose.
"""

import io
import unittest
from unittest.mock import AsyncMock, patch

from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject
from app.core.constants import (
    NOTES_SOURCE_TEXT_MAX_CHARACTERS,
    NOTES_SOURCE_TEXT_MIN_CHARACTERS,
)

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


def _add_text_page(writer: PdfWriter, text: str | None) -> None:
    page = writer.add_blank_page(width=200, height=200)

    if not text:
        # No /Contents at all -> pypdf extracts "" for this page.
        return

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


def make_pdf_bytes(pages_text: list[str | None]) -> bytes:
    """Build a minimal in-memory PDF with the given per-page text."""
    writer = PdfWriter()
    for text in pages_text:
        _add_text_page(writer, text)

    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


def make_encrypted_pdf_bytes() -> bytes:
    writer = PdfWriter()
    _add_text_page(writer, "secret content")
    writer.encrypt(user_password="secret123", owner_password="owner456")

    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


def make_long_text_pdf_bytes(character_count: int) -> bytes:
    """Build a PDF whose single page contains at least character_count chars."""
    # PDF literal strings must avoid unescaped parentheses; repeat a safe word.
    filler = ("word " * ((character_count // 5) + 20)).strip()
    return make_pdf_bytes([filler])


class FakeUploadFile:
    """Minimal stand-in for fastapi.UploadFile with an async .read(size)."""

    def __init__(self, data: bytes):
        self._data = data
        self.read = AsyncMock(side_effect=self._read)

    async def _read(self, size: int = -1) -> bytes:
        if size is None or size < 0:
            return self._data
        return self._data[:size]


def run_async(coro):
    import asyncio

    return asyncio.run(coro)


class ExtractSuccessTests(unittest.TestCase):
    def test_single_page_extraction(self):
        pdf_bytes = make_pdf_bytes(
            ["Photosynthesis converts light energy into chemical energy in plants."]
        )
        result = run_async(document_service.extract_text(FakeUploadFile(pdf_bytes)))

        self.assertIn("Photosynthesis", result.extracted_text)
        self.assertEqual(result.page_count, 1)
        self.assertEqual(result.character_count, len(result.extracted_text))

    def test_multi_page_extraction_preserves_order(self):
        pdf_bytes = make_pdf_bytes(
            [
                "Chapter one covers the fundamentals of the topic in detail.",
                "Chapter two builds on those fundamentals with more depth.",
            ]
        )
        result = run_async(document_service.extract_text(FakeUploadFile(pdf_bytes)))

        first_index = result.extracted_text.find("Chapter one")
        second_index = result.extracted_text.find("Chapter two")

        self.assertNotEqual(first_index, -1)
        self.assertNotEqual(second_index, -1)
        self.assertLess(first_index, second_index)
        self.assertEqual(result.page_count, 2)

    def test_page_count_matches_reported_pages(self):
        pdf_bytes = make_pdf_bytes(
            [
                "First page with enough filler text to be meaningful here.",
                "Second page with enough filler text to be meaningful here.",
                "Third page with enough filler text to be meaningful here.",
            ]
        )
        result = run_async(document_service.extract_text(FakeUploadFile(pdf_bytes)))
        self.assertEqual(result.page_count, 3)

    def test_pages_joined_with_double_newline(self):
        pdf_bytes = make_pdf_bytes(
            [
                "Alpha section text that is long enough to pass validation limits.",
                "Beta section text that is also long enough to pass validation limits.",
            ]
        )
        result = run_async(document_service.extract_text(FakeUploadFile(pdf_bytes)))
        self.assertIn("\n\n", result.extracted_text)

    def test_character_count_matches_trimmed_text_length(self):
        pdf_bytes = make_pdf_bytes(
            ["Some reasonably long sentence used purely for length checking here."]
        )
        result = run_async(document_service.extract_text(FakeUploadFile(pdf_bytes)))
        self.assertEqual(result.character_count, len(result.extracted_text.strip()))
        self.assertEqual(result.extracted_text, result.extracted_text.strip())


class ExtractErrorTests(unittest.TestCase):
    def test_empty_upload_raises_empty_file_error(self):
        with self.assertRaises(DocumentEmptyFileError):
            run_async(document_service.extract_text(FakeUploadFile(b"")))

    def test_oversized_upload_raises_too_large_error(self):
        original_limit = document_service.settings.max_pdf_size_bytes
        document_service.settings.max_pdf_size_bytes = 100
        try:
            oversized = b"%PDF-1.4\n" + (b"0" * 500)
            with self.assertRaises(DocumentTooLargeError):
                run_async(document_service.extract_text(FakeUploadFile(oversized)))
        finally:
            document_service.settings.max_pdf_size_bytes = original_limit

    def test_invalid_signature_raises_invalid_type_error(self):
        not_a_pdf = b"this is definitely not a pdf file at all"
        with self.assertRaises(DocumentInvalidTypeError):
            run_async(document_service.extract_text(FakeUploadFile(not_a_pdf)))

    def test_pdf_like_filename_with_invalid_bytes_is_rejected(self):
        # Content validation is signature-based, independent of filename;
        # this simulates a .pdf-named upload whose bytes are not a PDF.
        fake_content = b"NOT-A-REAL-PDF-BODY"
        with self.assertRaises(DocumentInvalidTypeError):
            run_async(document_service.extract_text(FakeUploadFile(fake_content)))

    def test_malformed_pdf_raises_parsing_error(self):
        malformed = b"%PDF-1.4\n" + b"\x00\x01\x02garbage not really a pdf structure"
        with self.assertRaises(DocumentParsingError):
            run_async(document_service.extract_text(FakeUploadFile(malformed)))

    def test_encrypted_pdf_raises_encrypted_error(self):
        encrypted_bytes = make_encrypted_pdf_bytes()
        with self.assertRaises(DocumentEncryptedError):
            run_async(document_service.extract_text(FakeUploadFile(encrypted_bytes)))

    def test_image_only_pdf_raises_no_text_error(self):
        blank_pdf = make_pdf_bytes([None])
        with self.assertRaises(DocumentNoTextError):
            run_async(document_service.extract_text(FakeUploadFile(blank_pdf)))

    def test_whitespace_only_extraction_raises_no_text_error(self):
        # A page containing only a space character extracts to whitespace,
        # which must be treated the same as "no usable text".
        whitespace_pdf = make_pdf_bytes([" "])
        with self.assertRaises(DocumentNoTextError):
            run_async(document_service.extract_text(FakeUploadFile(whitespace_pdf)))

    def test_text_below_notes_minimum_raises_too_short_error(self):
        short_pdf = make_pdf_bytes(["short"])
        with self.assertRaises(DocumentTextTooShortError):
            run_async(document_service.extract_text(FakeUploadFile(short_pdf)))

    def test_text_above_notes_maximum_raises_too_long_error(self):
        long_pdf = make_long_text_pdf_bytes(
            NOTES_SOURCE_TEXT_MAX_CHARACTERS + 500
        )
        with self.assertRaises(DocumentTextTooLongError):
            run_async(document_service.extract_text(FakeUploadFile(long_pdf)))

    def test_unexpected_reader_programming_error_propagates(self):
        valid_pdf = make_pdf_bytes(
            ["Enough source text to pass the minimum validation requirement."]
        )

        with patch.object(
            document_service,
            "PdfReader",
            side_effect=AttributeError("simulated programming error"),
        ):
            with self.assertRaises(AttributeError):
                run_async(
                    document_service.extract_text(FakeUploadFile(valid_pdf))
                )

    def test_unexpected_page_extraction_error_propagates(self):
        class BrokenPage:
            def extract_text(self):
                raise TypeError("simulated programming error")

        class FakeReader:
            is_encrypted = False
            pages = [BrokenPage()]

        valid_pdf = make_pdf_bytes(
            ["Enough source text to pass the minimum validation requirement."]
        )

        with patch.object(
            document_service,
            "PdfReader",
            return_value=FakeReader(),
        ):
            with self.assertRaises(TypeError):
                run_async(
                    document_service.extract_text(FakeUploadFile(valid_pdf))
                )

    def test_document_service_uses_shared_notes_limits(self):
        self.assertFalse(hasattr(document_service, "NOTES_MIN_CHARACTERS"))
        self.assertFalse(hasattr(document_service, "NOTES_MAX_CHARACTERS"))

        self.assertEqual(NOTES_SOURCE_TEXT_MIN_CHARACTERS, 50)
        self.assertEqual(NOTES_SOURCE_TEXT_MAX_CHARACTERS, 20_000)


if __name__ == "__main__":
    unittest.main()
