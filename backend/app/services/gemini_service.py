"""Gemini SDK integration for structured notes responses."""

import asyncio
import logging
import time
from typing import Any, TypeVar

from google import genai
from google.genai import errors
from pydantic import BaseModel, ValidationError

from app.core.config import settings
from app.schemas.notes import GeneratedNotesContent
from app.services.gemini_errors import (
    GeminiConfigurationError,
    GeminiInvalidResponseError,
    GeminiTimeoutError,
    GeminiUpstreamError,
)

logger = logging.getLogger(__name__)
StructuredResponseT = TypeVar("StructuredResponseT", bound=BaseModel)


class GeminiService:
    """Lazy wrapper around the official Google GenAI SDK."""

    def __init__(self) -> None:
        self._client: genai.Client | None = None
        self.last_metadata: dict[str, Any] = {}

    def _get_client(self) -> genai.Client:
        if not settings.gemini_api_key:
            raise GeminiConfigurationError("Gemini API key is not configured.")

        if self._client is None:
            self._client = genai.Client(api_key=settings.gemini_api_key)

        return self._client

    async def generate_structured_content(
        self,
        prompt: str,
        response_schema: type[StructuredResponseT],
    ) -> StructuredResponseT:
        """Generate and validate structured Gemini output for a Pydantic schema."""
        client = self._get_client()
        response = None
        max_attempts = 3
        backoff_sec = 2.0

        for attempt in range(max_attempts):
            try:
                start_time = time.time()
                response = await asyncio.wait_for(
                    client.aio.models.generate_content(
                        model=settings.gemini_model,
                        contents=prompt,
                        config={
                            "response_mime_type": "application/json",
                            "response_schema": response_schema,
                        },
                    ),
                    timeout=settings.gemini_timeout_seconds,
                )
                elapsed = time.time() - start_time
                
                prompt_tokens = 0
                candidates_tokens = 0
                if hasattr(response, "usage_metadata") and response.usage_metadata:
                    prompt_tokens = getattr(response.usage_metadata, "prompt_token_count", 0)
                    candidates_tokens = getattr(response.usage_metadata, "candidates_token_count", 0)
                elif hasattr(response, "usage") and response.usage:
                    prompt_tokens = getattr(response.usage, "prompt_tokens", 0)
                    candidates_tokens = getattr(response.usage, "completion_tokens", 0)
                
                self.last_metadata = {
                    "latency": elapsed,
                    "prompt_tokens": prompt_tokens,
                    "output_tokens": candidates_tokens,
                    "total_tokens": prompt_tokens + candidates_tokens
                }
                
                logger.info(
                    "Gemini generation complete: latency=%.2fs, prompt_tokens=%s, output_tokens=%s",
                    elapsed, prompt_tokens, candidates_tokens
                )
                break
            except asyncio.TimeoutError as exc:
                logger.warning(
                    "Gemini request timed out after %s seconds.",
                    settings.gemini_timeout_seconds,
                )
                raise GeminiTimeoutError("Gemini request timed out.") from exc
            except errors.APIError as exc:
                code = getattr(exc, "code", None)
                status = getattr(exc, "status", "")
                if (code == 429 or status == "RESOURCE_EXHAUSTED") and attempt < max_attempts - 1:
                    logger.warning(
                        "Gemini rate limit hit (RESOURCE_EXHAUSTED). Retrying in %.1fs... (Attempt %d/%d)",
                        backoff_sec, attempt + 1, max_attempts
                    )
                    await asyncio.sleep(backoff_sec)
                    backoff_sec *= 2.0
                    continue
                
                logger.error(
                    "Gemini upstream error: code=%s status=%s",
                    code or "unknown",
                    status or "unknown",
                )
                raise GeminiUpstreamError("Gemini request failed.") from exc

        if response is None:
            raise GeminiUpstreamError("Gemini request failed to return a response.")

        return self._validate_parsed_response_for_schema(
            getattr(response, "parsed", None),
            response_schema,
        )

    async def generate_notes_content(self, prompt: str) -> GeneratedNotesContent:
        return await self.generate_structured_content(prompt, GeneratedNotesContent)

    @staticmethod
    def _validate_parsed_response(parsed: Any) -> GeneratedNotesContent:
        return GeminiService._validate_parsed_response_for_schema(
            parsed,
            GeneratedNotesContent,
        )

    @staticmethod
    def _validate_parsed_response_for_schema(
        parsed: Any,
        response_schema: type[StructuredResponseT],
    ) -> StructuredResponseT:
        if parsed is None:
            logger.error("Gemini returned no parsed structured response.")
            raise GeminiInvalidResponseError("Gemini response was not parsed.")

        if isinstance(parsed, response_schema):
            return parsed

        try:
            return response_schema.model_validate(parsed)
        except ValidationError as exc:
            logger.error("Gemini structured response failed schema validation.")
            raise GeminiInvalidResponseError(
                "Gemini response failed validation."
            ) from exc


gemini_service = GeminiService()
