"""Pydantic schemas for focused weak-concept revision."""

from pydantic import BaseModel, Field, field_validator

from app.schemas.notes import NotesResponse


def _normalize_required_text(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Value must be a string.")

    normalized = value.strip()
    if not normalized:
        raise ValueError("Value cannot be empty.")

    return normalized


def _normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("Value must be a string.")

    normalized = value.strip()
    return normalized or None


def _deduplicate_normalized_text(values: list[str]) -> list[str]:
    if not isinstance(values, list):
        raise ValueError("Value must be a list of strings.")

    deduplicated: list[str] = []
    seen: set[str] = set()

    for value in values:
        normalized = _normalize_required_text(value)
        key = normalized.casefold()
        if key not in seen:
            seen.add(key)
            deduplicated.append(normalized)

    if not deduplicated:
        raise ValueError("At least one value is required.")

    return deduplicated


class IncorrectQuestionContext(BaseModel):
    concept: str = Field(min_length=1, max_length=160)
    question: str = Field(min_length=1, max_length=1_000)
    selected_answer: str = Field(min_length=1, max_length=500)
    correct_answer: str = Field(min_length=1, max_length=500)
    explanation: str = Field(min_length=1, max_length=1_000)

    @field_validator(
        "concept",
        "question",
        "selected_answer",
        "correct_answer",
        "explanation",
        mode="before",
    )
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return _normalize_required_text(value)


class RevisionRequest(BaseModel):
    notes_response: NotesResponse
    weak_concepts: list[str] = Field(min_length=1)
    incorrect_questions: list[IncorrectQuestionContext] = Field(min_length=1)

    @field_validator("weak_concepts", mode="before")
    @classmethod
    def normalize_weak_concepts(cls, value: list[str]) -> list[str]:
        return _deduplicate_normalized_text(value)


class ConceptRevision(BaseModel):
    concept: str = Field(min_length=1, max_length=160)
    explanation: str = Field(min_length=1)
    example: str = Field(min_length=1)
    analogy: str | None = None
    memory_trick: str | None = None
    key_facts: list[str] = Field(min_length=1)
    common_mistake: str | None = None

    @field_validator("concept", "explanation", "example", mode="before")
    @classmethod
    def normalize_required_text(cls, value: str) -> str:
        return _normalize_required_text(value)

    @field_validator("analogy", "memory_trick", "common_mistake", mode="before")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        return _normalize_optional_text(value)

    @field_validator("key_facts", mode="before")
    @classmethod
    def normalize_key_facts(cls, value: list[str]) -> list[str]:
        return _deduplicate_normalized_text(value)


class RevisionResponse(BaseModel):
    concepts: list[ConceptRevision] = Field(min_length=1)
