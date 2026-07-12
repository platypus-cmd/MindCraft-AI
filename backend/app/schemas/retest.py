"""Pydantic schemas for targeted weak-concept retests."""

from pydantic import BaseModel, Field, field_validator

from app.schemas.notes import NotesResponse


def normalize_required_text(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Value must be a string.")

    normalized = value.strip()
    if not normalized:
        raise ValueError("Value cannot be empty.")

    return normalized


def deduplicate_case_insensitive(values: list[str]) -> list[str]:
    if not isinstance(values, list):
        raise ValueError("Value must be a list of strings.")

    deduplicated: list[str] = []
    seen: set[str] = set()

    for value in values:
        normalized = normalize_required_text(value)
        key = normalized.casefold()
        if key not in seen:
            seen.add(key)
            deduplicated.append(normalized)

    if not deduplicated:
        raise ValueError("At least one value is required.")

    return deduplicated


def deduplicate_exact_normalized(values: list[str]) -> list[str]:
    if not isinstance(values, list):
        raise ValueError("Value must be a list of strings.")

    deduplicated: list[str] = []
    seen: set[str] = set()

    for value in values:
        normalized = normalize_required_text(value)
        if normalized not in seen:
            seen.add(normalized)
            deduplicated.append(normalized)

    if not deduplicated:
        raise ValueError("At least one value is required.")

    return deduplicated


class RetestRequest(BaseModel):
    notes_response: NotesResponse
    weak_concepts: list[str] = Field(min_length=1)
    original_questions: list[str] = Field(min_length=1)

    @field_validator("weak_concepts", mode="before")
    @classmethod
    def normalize_weak_concepts(cls, value: list[str]) -> list[str]:
        return deduplicate_case_insensitive(value)

    @field_validator("original_questions", mode="before")
    @classmethod
    def normalize_original_questions(cls, value: list[str]) -> list[str]:
        return deduplicate_exact_normalized(value)
