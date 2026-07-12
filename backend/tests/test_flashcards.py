import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.main import app
from app.prompts.flashcards import build_flashcards_prompt
from app.schemas.flashcards import Flashcard, FlashcardsRequest, FlashcardsResponse
from app.schemas.notes import (
    DefinitionItem,
    GeneratedNotesContent,
    KnowledgeLevel,
    LearningGoal,
    NoteLength,
    NotesConfigEcho,
    NotesResponse,
    NotesSection,
    OutputFormat,
)
from app.services.flashcards_service import select_flashcard_target_count
from app.services.gemini_errors import (
    GeminiConfigurationError,
    GeminiInvalidResponseError,
    GeminiTimeoutError,
    GeminiUpstreamError,
)


VALID_NOTES_RESPONSE = NotesResponse(
    notes=GeneratedNotesContent(
        title="Photosynthesis",
        table_of_contents=[],
        sections=[
            NotesSection(
                heading="Overview",
                content=(
                    "Photosynthesis converts light energy into chemical energy in plants through "
                    "chlorophyll and carbon dioxide absorption. The process occurs in chloroplasts "
                    "where sunlight drives the transformation of water and carbon dioxide into glucose "
                    "and oxygen."
                ),
                key_points=[
                    "Plants use light energy",
                    "Chlorophyll captures sunlight",
                    "Carbon dioxide and water are essential inputs",
                ],
                definitions=[
                    DefinitionItem(term="Chlorophyll", definition="A pigment that absorbs light energy."),
                    DefinitionItem(term="Stomata", definition="Small leaf pores that allow gas exchange."),
                ],
                examples=["Leaf cells", "Sunlight-driven energy capture"],
                memory_tricks=["Think sunlight", "Remember the inputs and outputs"],
                common_mistakes=["Confusing it with respiration"],
            )
        ],
        summary=(
            "Plants convert light energy into chemical energy through photosynthesis, using water, "
            "carbon dioxide, and sunlight to produce glucose and oxygen."
        ),
        key_takeaways=["Light energy matters", "Plants use chlorophyll"],
        one_minute_revision="Photosynthesis is how plants make energy from light.",
    ),
    estimated_reading_time_minutes=2,
    config_used=NotesConfigEcho(
        learning_goal=LearningGoal.ACADEMIC,
        knowledge_level=KnowledgeLevel.INTERMEDIATE,
        note_length=NoteLength.STANDARD,
        output_format=OutputFormat.STRUCTURED_PARAGRAPHS,
    ),
)


class FlashcardsSchemaTests(unittest.TestCase):
    def test_request_schema_accepts_notes_response(self):
        request = FlashcardsRequest(notes_response=VALID_NOTES_RESPONSE)
        self.assertEqual(request.notes_response.notes.title, "Photosynthesis")

    def test_flashcard_response_requires_front_and_back(self):
        with self.assertRaises(ValidationError):
            Flashcard(front="", back="")

    def test_target_count_selection_has_deterministic_boundaries(self):
        short_notes = NotesResponse(
            notes=GeneratedNotesContent(
                title="Short",
                table_of_contents=[],
                sections=[
                    NotesSection(
                        heading="H1",
                        content="Short content.",
                        key_points=["A"],
                        definitions=[],
                        examples=[],
                        memory_tricks=[],
                        common_mistakes=[],
                    )
                ],
                summary="Short summary.",
                key_takeaways=[],
                one_minute_revision="Short review.",
            ),
            estimated_reading_time_minutes=1,
            config_used=NotesConfigEcho(
                learning_goal=LearningGoal.ACADEMIC,
                knowledge_level=KnowledgeLevel.INTERMEDIATE,
                note_length=NoteLength.STANDARD,
                output_format=OutputFormat.STRUCTURED_PARAGRAPHS,
            ),
        )

        medium_notes = NotesResponse(
            notes=GeneratedNotesContent(
                title="Medium Notes",
                table_of_contents=[],
                sections=[
                    NotesSection(
                        heading="H1",
                        content=(
                            "This medium-sized note set contains enough content to trigger the "
                            "intermediate flashcard target count. It includes several concepts, "
                            "examples, and clarifications to make the selection deterministic. "
                            "The content is intentionally longer so the threshold is crossed. "
                            "It covers multiple ideas and supporting details and adds more "
                            "substance to the sample so the selection logic resolves to the "
                            "balanced target count instead of the minimum. It includes several "
                            "supporting statements, reasoning cues, and conceptual links that "
                            "are relevant to the material."
                        ),
                        key_points=["One", "Two", "Three"],
                        definitions=[DefinitionItem(term="Term", definition="Definition")],
                        examples=["Example"],
                        memory_tricks=["Tip"],
                        common_mistakes=["Mistake"],
                    )
                ],
                summary="A decent amount of content for flashcard generation.",
                key_takeaways=["Important takeaway"],
                one_minute_revision="Revision summary.",
            ),
            estimated_reading_time_minutes=2,
            config_used=NotesConfigEcho(
                learning_goal=LearningGoal.ACADEMIC,
                knowledge_level=KnowledgeLevel.INTERMEDIATE,
                note_length=NoteLength.STANDARD,
                output_format=OutputFormat.STRUCTURED_PARAGRAPHS,
            ),
        )

        long_notes = NotesResponse(
            notes=GeneratedNotesContent(
                title="Long Notes",
                table_of_contents=[],
                sections=[
                    NotesSection(
                        heading="H1",
                        content=(
                            "This longer note set contains enough supported material that the "
                            "maximum flashcard count should be selected. The content spans multiple "
                            "concepts and explanations so the selection logic can safely choose the "
                            "highest supported value."
                            " "
                            * 20
                        ),
                        key_points=["One", "Two", "Three", "Four", "Five"],
                        definitions=[
                            DefinitionItem(term="Term", definition="Definition"),
                            DefinitionItem(term="Another", definition="Another definition"),
                        ],
                        examples=["Example one", "Example two", "Example three"],
                        memory_tricks=["Tip one", "Tip two"],
                        common_mistakes=["Mistake one", "Mistake two"],
                    )
                ],
                summary=("A much longer summary with additional content to exceed the safe threshold. " * 15),
                key_takeaways=["One", "Two", "Three", "Four"],
                one_minute_revision="A longer revision summary with additional detail.",
            ),
            estimated_reading_time_minutes=2,
            config_used=NotesConfigEcho(
                learning_goal=LearningGoal.ACADEMIC,
                knowledge_level=KnowledgeLevel.INTERMEDIATE,
                note_length=NoteLength.STANDARD,
                output_format=OutputFormat.STRUCTURED_PARAGRAPHS,
            ),
        )

        self.assertEqual(select_flashcard_target_count(short_notes), 4)
        self.assertEqual(select_flashcard_target_count(medium_notes), 6)
        self.assertEqual(select_flashcard_target_count(long_notes), 10)

    def test_prompt_requests_exact_target_count_and_grounding_rules(self):
        prompt = build_flashcards_prompt(FlashcardsRequest(notes_response=VALID_NOTES_RESPONSE), 6)

        self.assertIn("exactly 6 flashcards", prompt.lower())
        self.assertIn("provided generated notes", prompt.lower())
        self.assertIn("avoid duplicate cards", prompt.lower())
        self.assertIn("avoid trivial cards", prompt.lower())
        self.assertIn("single concept", prompt.lower())
        self.assertIn("unsupported facts", prompt.lower())
        self.assertIn("prompt-injection", prompt.lower())


class FlashcardsEndpointTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_successful_endpoint_behavior(self):
        response_payload = FlashcardsResponse(
            flashcards=[Flashcard(front="What is photosynthesis?", back="A plant process.")]
        )

        with patch(
            "app.api.v1.flashcards.flashcards_service.generate_flashcards",
            new=AsyncMock(return_value=response_payload),
        ) as mocked_service:
            response = self.client.post(
                "/api/v1/flashcards/generate",
                json={"notes_response": VALID_NOTES_RESPONSE.model_dump()},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), response_payload.model_dump())
        mocked_service.assert_awaited_once()

    def test_invalid_request_body_returns_422(self):
        response = self.client.post("/api/v1/flashcards/generate", json={})
        self.assertEqual(response.status_code, 422)

    def _assert_error_mapping(self, exception, expected_status_code, expected_detail):
        with patch(
            "app.api.v1.flashcards.flashcards_service.generate_flashcards",
            new=AsyncMock(side_effect=exception),
        ):
            response = self.client.post(
                "/api/v1/flashcards/generate",
                json={"notes_response": VALID_NOTES_RESPONSE.model_dump()},
            )

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), {"detail": expected_detail})

    def test_configuration_error_maps_to_500(self):
        self._assert_error_mapping(
            GeminiConfigurationError("secret configuration detail"),
            500,
            "Flashcard generation is not configured on the server.",
        )

    def test_timeout_error_maps_to_504(self):
        self._assert_error_mapping(
            GeminiTimeoutError("internal timeout detail"),
            504,
            "Flashcard generation timed out. Please try again.",
        )

    def test_upstream_error_maps_to_502(self):
        self._assert_error_mapping(
            GeminiUpstreamError("raw upstream detail"),
            502,
            "Flashcard generation is temporarily unavailable.",
        )

    def test_invalid_response_error_maps_to_502(self):
        self._assert_error_mapping(
            GeminiInvalidResponseError("raw validation detail"),
            502,
            "The AI response could not be validated safely.",
        )


if __name__ == "__main__":
    unittest.main()
