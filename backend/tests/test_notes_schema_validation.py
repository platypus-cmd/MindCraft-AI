import unittest

from pydantic import ValidationError

from app.schemas.notes import NotesRequest


VALID_SOURCE = (
    "Photosynthesis is the process by which green plants use sunlight to synthesize "
    "food from carbon dioxide and water. It generally involves chlorophyll and releases "
    "oxygen as a byproduct."
)


def valid_payload(**overrides):
    payload = {
        "source_text": VALID_SOURCE,
        "learning_goal": "academic",
        "knowledge_level": "intermediate",
        "note_length": "standard",
        "output_format": "structured_paragraphs",
    }
    payload.update(overrides)
    return payload


class NotesRequestValidationTests(unittest.TestCase):
    def assert_invalid_payload(self, **overrides):
        with self.assertRaises(ValidationError):
            NotesRequest(**valid_payload(**overrides))

    def test_blank_source_text_is_rejected(self):
        self.assert_invalid_payload(source_text="   ")

    def test_source_text_shorter_than_50_characters_after_trimming_is_rejected(self):
        self.assert_invalid_payload(source_text="   too short for backend validation   ")

    def test_source_text_longer_than_20000_characters_after_trimming_is_rejected(self):
        self.assert_invalid_payload(source_text="a" * 20001)

    def test_source_text_is_trimmed_before_use(self):
        request = NotesRequest(**valid_payload(source_text=f"   {VALID_SOURCE}   "))

        self.assertEqual(request.source_text, VALID_SOURCE)

    def test_unsupported_learning_goal_is_rejected(self):
        self.assert_invalid_payload(learning_goal="casual")

    def test_unsupported_knowledge_level_is_rejected(self):
        self.assert_invalid_payload(knowledge_level="expert")

    def test_unsupported_note_length_is_rejected(self):
        self.assert_invalid_payload(note_length="long")

    def test_unsupported_output_format_is_rejected(self):
        self.assert_invalid_payload(output_format="markdown")


if __name__ == "__main__":
    unittest.main()
