"""Pydantic schemas for quiz generation."""

from pydantic import BaseModel, Field, field_validator

from app.schemas.notes import NotesResponse


class QuizQuestion(BaseModel):
    question: str = Field(min_length=1)
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str = Field(min_length=1)
    explanation: str = Field(min_length=1)
    concept: str = Field(min_length=1)

    @field_validator("question", "correct_answer", "explanation", "concept", mode="before")
    @classmethod
    def normalize_and_validate_text(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("Quiz text must be a string.")

        normalized = value.strip()
        if not normalized:
            raise ValueError("Quiz text cannot be empty.")

        return normalized

    @field_validator("options", mode="before")
    @classmethod
    def validate_options(cls, value: list[str]) -> list[str]:
        if not isinstance(value, list):
            raise TypeError("Options must be a list of strings.")

        normalized = [item.strip() for item in value]
        if len(normalized) != 4:
            raise ValueError("Quiz questions must have exactly four options.")
        if not all(normalized):
            raise ValueError("Quiz options cannot be empty.")
        return normalized

    @field_validator("correct_answer", mode="after")
    @classmethod
    def validate_correct_answer(cls, value: str, info) -> str:
        if info.data.get("options") is not None and value not in info.data["options"]:
            raise ValueError("Correct answer must be one of the provided options.")
        return value


from typing import Literal

class QuizRequest(BaseModel):
    notes_response: NotesResponse
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    count: Literal[5, 10, 15, 20] = 10


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(min_length=1)
