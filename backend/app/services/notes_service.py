"""Orchestration service for the notes vertical slice."""

import math
import re
from typing import Any

from pydantic import BaseModel

from app.prompts.notes import build_notes_prompt
from app.schemas.notes import GeneratedNotesContent, NotesConfigEcho, NotesRequest, NotesResponse
from app.services.gemini_service import gemini_service

WORDS_PER_MINUTE = 200


def _collect_text(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]

    if isinstance(value, BaseModel):
        return _collect_text(value.model_dump())

    if isinstance(value, dict):
        text_parts: list[str] = []
        for item in value.values():
            text_parts.extend(_collect_text(item))
        return text_parts

    if isinstance(value, list):
        text_parts: list[str] = []
        for item in value:
            text_parts.extend(_collect_text(item))
        return text_parts

    return []


def estimate_reading_time_minutes(notes: GeneratedNotesContent) -> int:
    """Estimate reading time from generated text using 200 words per minute."""
    combined_text = " ".join(_collect_text(notes))
    word_count = len(re.findall(r"\b[\w'-]+\b", combined_text))

    if word_count == 0:
        return 0

    return max(1, math.ceil(word_count / WORDS_PER_MINUTE))


async def generate_notes(request: NotesRequest) -> NotesResponse:
    prompt = build_notes_prompt(request)
    notes = await gemini_service.generate_notes_content(prompt)
    estimated_reading_time = estimate_reading_time_minutes(notes)

    return NotesResponse(
        notes=notes,
        estimated_reading_time_minutes=estimated_reading_time,
        config_used=NotesConfigEcho(
            learning_goal=request.learning_goal,
            knowledge_level=request.knowledge_level,
            note_length=request.note_length,
            output_format=request.output_format,
        ),
    )
