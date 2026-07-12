import io
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from pypdf import PdfReader

from app.main import app
from app.schemas.notes import NotesResponse
from app.services import notes_export_service


NOTES_RESPONSE_PAYLOAD = {
    "notes": {
        "title": "Photosynthesis Study Notes",
        "table_of_contents": [
            "Photosynthesis Overview",
            "Chlorophyll and Energy Conversion",
        ],
        "sections": [
            {
                "heading": "Photosynthesis Overview",
                "content": (
                    "Photosynthesis converts light energy into chemical energy "
                    "stored in glucose."
                ),
                "key_points": [
                    "Plants use carbon dioxide, water, and sunlight.",
                    "Oxygen is released as a byproduct.",
                ],
                "definitions": [
                    {
                        "term": "Chlorophyll",
                        "definition": "A green pigment that captures light energy.",
                    }
                ],
                "examples": [
                    "Green leaves making glucose during daylight."
                ],
                "memory_tricks": [
                    "Light plus leaves leads to food."
                ],
                "common_mistakes": [
                    "Assuming photosynthesis happens only because of soil."
                ],
            }
        ],
        "summary": "Plants convert light energy into stored chemical energy.",
        "key_takeaways": [
            "Photosynthesis supports plant food production.",
            "Chlorophyll is central to capturing sunlight.",
        ],
        "one_minute_revision": (
            "Photosynthesis uses light, carbon dioxide, and water to make glucose."
        ),
    },
    "estimated_reading_time_minutes": 3,
    "config_used": {
        "learning_goal": "academic",
        "knowledge_level": "intermediate",
        "note_length": "comprehensive",
        "output_format": "structured_paragraphs",
    },
}


def make_notes_response() -> NotesResponse:
    return NotesResponse(**NOTES_RESPONSE_PAYLOAD)


def extract_pdf_text(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


class NotesExportServiceTests(unittest.TestCase):
    def test_successful_pdf_generation_returns_non_empty_pdf_bytes(self):
        pdf_bytes = notes_export_service.generate_notes_pdf(make_notes_response())

        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)
        self.assertTrue(pdf_bytes.startswith(b"%PDF-"))

    def test_generated_pdf_is_parseable_and_contains_complete_notes_content(self):
        pdf_bytes = notes_export_service.generate_notes_pdf(make_notes_response())
        extracted_text = extract_pdf_text(pdf_bytes)

        expected_text = [
            "Photosynthesis Study Notes",
            "Estimated reading time: 3 minute(s)",
            "Photosynthesis Overview",
            "Chlorophyll and Energy Conversion",
            "Photosynthesis converts light energy into chemical energy",
            "Plants use carbon dioxide, water, and sunlight.",
            "Chlorophyll",
            "A green pigment that captures light energy.",
            "Green leaves making glucose during daylight.",
            "Light plus leaves leads to food.",
            "Assuming photosynthesis happens only because of soil.",
            "Plants convert light energy into stored chemical energy.",
            "Photosynthesis supports plant food production.",
            "Photosynthesis uses light, carbon dioxide, and water to make glucose.",
        ]

        for text in expected_text:
            self.assertIn(text, extracted_text)

    def test_pdf_generation_does_not_call_gemini(self):
        with patch("app.services.notes_service.gemini_service") as mock_gemini_service:
            pdf_bytes = notes_export_service.generate_notes_pdf(make_notes_response())

        self.assertTrue(pdf_bytes.startswith(b"%PDF-"))
        mock_gemini_service.generate_notes_content.assert_not_called()

    def test_unexpected_programming_errors_are_not_swallowed(self):
        with patch.object(
            notes_export_service,
            "_build_story",
            side_effect=RuntimeError("simulated programming error"),
        ):
            with self.assertRaises(RuntimeError):
                notes_export_service.generate_notes_pdf(make_notes_response())


class NotesExportEndpointTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_valid_notes_response_returns_pdf_download(self):
        response = self.client.post(
            "/api/v1/notes/export/pdf",
            json=NOTES_RESPONSE_PAYLOAD,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/pdf")
        self.assertEqual(
            response.headers["content-disposition"],
            'attachment; filename="mindcraft-notes.pdf"',
        )
        self.assertTrue(response.content.startswith(b"%PDF-"))

        extracted_text = extract_pdf_text(response.content)
        self.assertIn("Photosynthesis Study Notes", extracted_text)
        self.assertIn("Photosynthesis converts light energy", extracted_text)
        self.assertIn("Photosynthesis supports plant food production.", extracted_text)

    def test_invalid_request_body_returns_422(self):
        response = self.client.post(
            "/api/v1/notes/export/pdf",
            json={"unexpected": "shape"},
        )

        self.assertEqual(response.status_code, 422)

    def test_missing_required_nested_content_returns_422(self):
        payload = {
            **NOTES_RESPONSE_PAYLOAD,
            "notes": {
                **NOTES_RESPONSE_PAYLOAD["notes"],
                "sections": [
                    {
                        **NOTES_RESPONSE_PAYLOAD["notes"]["sections"][0],
                        "content": None,
                    }
                ],
            },
        }

        response = self.client.post(
            "/api/v1/notes/export/pdf",
            json=payload,
        )

        self.assertEqual(response.status_code, 422)

    def test_export_endpoint_does_not_call_gemini_or_regenerate_notes(self):
        with (
            patch("app.services.notes_service.gemini_service") as mock_gemini_service,
            patch("app.api.v1.notes.notes_service.generate_notes") as mock_generate_notes,
        ):
            response = self.client.post(
                "/api/v1/notes/export/pdf",
                json=NOTES_RESPONSE_PAYLOAD,
            )

        self.assertEqual(response.status_code, 200)
        mock_gemini_service.generate_notes_content.assert_not_called()
        mock_generate_notes.assert_not_called()

    def test_unexpected_service_errors_are_not_converted_to_success_or_domain_error(self):
        with patch(
            "app.api.v1.notes.notes_export_service.generate_notes_pdf",
            side_effect=RuntimeError("simulated programming error"),
        ):
            with self.assertRaises(RuntimeError):
                self.client.post(
                    "/api/v1/notes/export/pdf",
                    json=NOTES_RESPONSE_PAYLOAD,
                )


if __name__ == "__main__":
    unittest.main()
