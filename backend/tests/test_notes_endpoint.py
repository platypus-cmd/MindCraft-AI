import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.services.gemini_errors import (
    GeminiConfigurationError,
    GeminiInvalidResponseError,
    GeminiTimeoutError,
    GeminiUpstreamError,
)


VALID_PAYLOAD = {
    "source_text": (
        "Photosynthesis is the biological process used by plants to convert light energy "
        "into chemical energy. Chlorophyll captures sunlight, carbon dioxide enters leaves "
        "through stomata, and water is absorbed by roots."
    ),
    "learning_goal": "academic",
    "knowledge_level": "intermediate",
    "note_length": "standard",
    "output_format": "structured_paragraphs",
}


class NotesEndpointErrorMappingTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def _assert_error_mapping(
        self,
        exception,
        expected_status_code,
        expected_detail,
    ):
        with patch(
            "app.api.v1.notes.notes_service.generate_notes",
            new=AsyncMock(side_effect=exception),
        ):
            response = self.client.post(
                "/api/v1/notes/generate",
                json=VALID_PAYLOAD,
            )

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(
            response.json(),
            {"detail": expected_detail},
        )

    def test_configuration_error_maps_to_500(self):
        self._assert_error_mapping(
            GeminiConfigurationError("secret internal configuration detail"),
            500,
            "Notes generation is not configured on the server.",
        )

    def test_timeout_error_maps_to_504(self):
        self._assert_error_mapping(
            GeminiTimeoutError("internal timeout detail"),
            504,
            "Notes generation timed out. Please try again.",
        )

    def test_upstream_error_maps_to_502(self):
        self._assert_error_mapping(
            GeminiUpstreamError("raw upstream detail"),
            502,
            "Notes generation is temporarily unavailable.",
        )

    def test_invalid_response_error_maps_to_502(self):
        self._assert_error_mapping(
            GeminiInvalidResponseError("raw validation detail"),
            502,
            "The AI response could not be validated safely.",
        )


if __name__ == "__main__":
    unittest.main()