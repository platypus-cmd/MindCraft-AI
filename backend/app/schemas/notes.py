"""Pydantic schemas for personalized notes generation."""

from enum import Enum

from pydantic import BaseModel, Field, field_validator

from app.core.constants import (
    NOTES_SOURCE_TEXT_MAX_CHARACTERS,
    NOTES_SOURCE_TEXT_MIN_CHARACTERS,
)


class LearningGoal(str, Enum):
    ACADEMIC = "academic"
    EXAM_REVISION = "exam_revision"
    DEEP_UNDERSTANDING = "deep_understanding"
    EXPLAIN_SIMPLY = "explain_simply"


class KnowledgeLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class NoteLength(str, Enum):
    QUICK_REVIEW = "quick_review"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"


class OutputFormat(str, Enum):
    STRUCTURED_PARAGRAPHS = "structured_paragraphs"
    BULLET_POINTS = "bullet_points"
    CORNELL_NOTES = "cornell_notes"
    OUTLINE = "outline"


class NotesRequest(BaseModel):
    source_text: str = Field(
        min_length=NOTES_SOURCE_TEXT_MIN_CHARACTERS,
        max_length=NOTES_SOURCE_TEXT_MAX_CHARACTERS,
    )
    learning_goal: LearningGoal
    knowledge_level: KnowledgeLevel
    note_length: NoteLength
    output_format: OutputFormat

    @field_validator("source_text", mode="before")
    @classmethod
    def trim_source_text(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value


class DefinitionItem(BaseModel):
    term: str
    definition: str


class NotesSection(BaseModel):
    heading: str
    content: str
    key_points: list[str]
    definitions: list[DefinitionItem]
    examples: list[str]
    memory_tricks: list[str]
    common_mistakes: list[str]


class GeneratedNotesContent(BaseModel):
    title: str
    table_of_contents: list[str]
    sections: list[NotesSection]
    summary: str
    key_takeaways: list[str]
    one_minute_revision: str


class NotesConfigEcho(BaseModel):
    learning_goal: LearningGoal
    knowledge_level: KnowledgeLevel
    note_length: NoteLength
    output_format: OutputFormat


class NotesResponse(BaseModel):
    notes: GeneratedNotesContent
    estimated_reading_time_minutes: int
    config_used: NotesConfigEcho
