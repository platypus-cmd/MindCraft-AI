"""Pydantic schemas for flashcard generation."""

from pydantic import BaseModel, Field, field_validator

from app.schemas.notes import NotesResponse


class Flashcard(BaseModel):
    front: str = Field(min_length=1)
    back: str = Field(min_length=1)

    @field_validator("front", "back", mode="before")
    @classmethod
    def normalize_and_validate_text(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("Flashcard text must be a string.")

        normalized = value.strip()
        if not normalized:
            raise ValueError("Flashcard text cannot be empty.")

        return normalized


class FlashcardsRequest(BaseModel):
    notes_response: NotesResponse


class FlashcardsResponse(BaseModel):
    flashcards: list[Flashcard] = Field(min_length=1)
