"""Flashcard generation service and deterministic target-count selection."""

import asyncio
import logging
from typing import Any

from google import genai
from google.genai import errors
from pydantic import ValidationError

from app.core.config import settings
from app.prompts.flashcards import build_flashcards_prompt
from app.schemas.flashcards import FlashcardsRequest, FlashcardsResponse
from app.schemas.notes import NotesResponse
from app.services.gemini_errors import (
    GeminiConfigurationError,
    GeminiInvalidResponseError,
    GeminiTimeoutError,
    GeminiUpstreamError,
)

logger = logging.getLogger(__name__)

MAX_FLASHCARDS = 10
MID_FLASHCARDS = 6
MIN_FLASHCARDS = 4


def _notes_text_length(notes_response: NotesResponse) -> int:
    parts = [
        notes_response.notes.title,
        notes_response.notes.summary,
        notes_response.notes.one_minute_revision,
        *notes_response.notes.key_takeaways,
    ]

    for section in notes_response.notes.sections:
        parts.extend(
            [
                section.heading,
                section.content,
                " ".join(section.key_points),
                " ".join(item.term for item in section.definitions),
                " ".join(item.definition for item in section.definitions),
                " ".join(section.examples),
                " ".join(section.memory_tricks),
                " ".join(section.common_mistakes),
            ]
        )

    return len(" ".join(part for part in parts if part))


def select_flashcard_target_count(notes_response: NotesResponse) -> int:
    """Choose a deterministic flashcard target count from the provided notes.

    Version 1 uses simple thresholds based on note substance rather than
    configurable quantity settings. Short notes receive a conservative count,
    medium notes receive a balanced count, and noticeably longer notes receive
    the safe maximum.
    """
    note_text_length = _notes_text_length(notes_response)

    if note_text_length < 700:
        return MIN_FLASHCARDS

    if note_text_length < 1400:
        return MID_FLASHCARDS

    return MAX_FLASHCARDS


class FlashcardsService:
    """Service wrapper for flashcard generation via Gemini structured output."""

    def __init__(self) -> None:
        self._client: genai.Client | None = None

    def _get_client(self) -> genai.Client:
        if not settings.gemini_api_key:
            raise GeminiConfigurationError("Gemini API key is not configured.")

        if self._client is None:
            self._client = genai.Client(api_key=settings.gemini_api_key)

        return self._client

    async def generate_flashcards(self, request: FlashcardsRequest) -> FlashcardsResponse:
        target_count = select_flashcard_target_count(request.notes_response)
        prompt = build_flashcards_prompt(request, target_count)
        client = self._get_client()

        try:
            response = await asyncio.wait_for(
                client.aio.models.generate_content(
                    model=settings.gemini_model,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": FlashcardsResponse,
                    },
                ),
                timeout=settings.gemini_timeout_seconds,
            )
        except asyncio.TimeoutError as exc:
            logger.warning(
                "Gemini request timed out after %s seconds.",
                settings.gemini_timeout_seconds,
            )
            raise GeminiTimeoutError("Gemini request timed out.") from exc
        except errors.APIError as exc:
            logger.error(
                "Gemini upstream error: code=%s status=%s",
                getattr(exc, "code", "unknown"),
                getattr(exc, "status", "unknown"),
            )
            raise GeminiUpstreamError("Gemini request failed.") from exc

        return self._validate_parsed_response(getattr(response, "parsed", None))

    @staticmethod
    def _validate_parsed_response(parsed: Any) -> FlashcardsResponse:
        if parsed is None:
            logger.error("Gemini returned no parsed structured response.")
            raise GeminiInvalidResponseError("Gemini response was not parsed.")

        if isinstance(parsed, FlashcardsResponse):
            return parsed

        try:
            return FlashcardsResponse.model_validate(parsed)
        except ValidationError as exc:
            logger.error("Gemini structured response failed schema validation.")
            raise GeminiInvalidResponseError("Gemini response failed validation.") from exc


flashcards_service = FlashcardsService()


async def generate_flashcards(request: FlashcardsRequest) -> FlashcardsResponse:
    """Generate flashcards from the provided notes response."""
    return await flashcards_service.generate_flashcards(request)
