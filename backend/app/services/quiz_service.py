"""Quiz generation service and deterministic target-count selection."""

import asyncio
import logging
from typing import Any

from google import genai
from google.genai import errors
from pydantic import ValidationError

from app.core.config import settings
from app.prompts.quiz import build_quiz_prompt
from app.schemas.notes import NotesResponse
from app.schemas.quiz import QuizRequest, QuizResponse
from app.services.gemini_errors import (
    GeminiConfigurationError,
    GeminiInvalidResponseError,
    GeminiTimeoutError,
    GeminiUpstreamError,
)

logger = logging.getLogger(__name__)



class QuizService:
    """Service wrapper for quiz generation via Gemini structured output."""

    def __init__(self) -> None:
        self._client: genai.Client | None = None

    def _get_client(self) -> genai.Client:
        if not settings.gemini_api_key:
            raise GeminiConfigurationError("Gemini API key is not configured.")

        if self._client is None:
            self._client = genai.Client(api_key=settings.gemini_api_key)

        return self._client

    async def generate_quiz(self, request: QuizRequest) -> QuizResponse:
        prompt = build_quiz_prompt(request)
        client = self._get_client()

        try:
            response = await asyncio.wait_for(
                client.aio.models.generate_content(
                    model=settings.gemini_model,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": QuizResponse,
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
    def _validate_parsed_response(parsed: Any) -> QuizResponse:
        if parsed is None:
            logger.error("Gemini returned no parsed structured response.")
            raise GeminiInvalidResponseError("Gemini response was not parsed.")

        if isinstance(parsed, QuizResponse):
            return parsed

        try:
            return QuizResponse.model_validate(parsed)
        except ValidationError as exc:
            logger.error("Gemini structured response failed schema validation.")
            raise GeminiInvalidResponseError("Gemini response failed validation.") from exc


quiz_service = QuizService()


async def generate_quiz(request: QuizRequest) -> QuizResponse:
    """Generate a quiz from the provided notes response."""
    return await quiz_service.generate_quiz(request)
