"""Tests for shared Gemini structured-output generation."""

import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from pydantic import BaseModel

from app.core.config import settings
from app.schemas.notes import GeneratedNotesContent
from app.services.gemini_errors import (
    GeminiConfigurationError,
    GeminiInvalidResponseError,
    GeminiTimeoutError,
    GeminiUpstreamError,
)
from app.services.gemini_service import GeminiService


class SampleStructuredResponse(BaseModel):
    value: str


class FakeGeminiClient:
    def __init__(self, parsed):
        self.aio = SimpleNamespace(
            models=SimpleNamespace(
                generate_content=AsyncMock(return_value=SimpleNamespace(parsed=parsed))
            )
        )


def run_async(coro):
    return asyncio.run(coro)


class GeminiStructuredOutputTests(unittest.TestCase):
    def setUp(self):
        self.original_api_key = settings.gemini_api_key
        self.original_model = settings.gemini_model
        self.original_timeout = settings.gemini_timeout_seconds
        settings.gemini_api_key = "test-key"
        settings.gemini_model = "test-model"
        settings.gemini_timeout_seconds = 12

    def tearDown(self):
        settings.gemini_api_key = self.original_api_key
        settings.gemini_model = self.original_model
        settings.gemini_timeout_seconds = self.original_timeout

    def test_generic_helper_success_returns_validated_model(self):
        client = FakeGeminiClient({"value": "ok"})
        service = GeminiService()

        with patch("app.services.gemini_service.genai.Client", return_value=client):
            result = run_async(
                service.generate_structured_content(
                    "prompt",
                    SampleStructuredResponse,
                )
            )

        self.assertIsInstance(result, SampleStructuredResponse)
        self.assertEqual(result.value, "ok")

    def test_supplied_response_schema_is_passed_to_sdk_config(self):
        client = FakeGeminiClient({"value": "ok"})
        service = GeminiService()

        with patch("app.services.gemini_service.genai.Client", return_value=client):
            run_async(
                service.generate_structured_content(
                    "prompt",
                    SampleStructuredResponse,
                )
            )

        call_kwargs = client.aio.models.generate_content.await_args.kwargs
        self.assertEqual(call_kwargs["config"]["response_schema"], SampleStructuredResponse)
        self.assertEqual(call_kwargs["config"]["response_mime_type"], "application/json")

    def test_lazy_client_initialization_is_preserved(self):
        client = FakeGeminiClient({"value": "ok"})
        service = GeminiService()

        with patch(
            "app.services.gemini_service.genai.Client",
            return_value=client,
        ) as mocked_client_factory:
            self.assertIsNone(service._client)
            run_async(service.generate_structured_content("prompt", SampleStructuredResponse))
            run_async(service.generate_structured_content("prompt", SampleStructuredResponse))

        mocked_client_factory.assert_called_once_with(api_key="test-key")

    def test_configured_model_and_timeout_are_used(self):
        client = FakeGeminiClient({"value": "ok"})
        service = GeminiService()
        captured_timeout = None

        async def fake_wait_for(awaitable, timeout):
            nonlocal captured_timeout
            captured_timeout = timeout
            return await awaitable

        with (
            patch("app.services.gemini_service.genai.Client", return_value=client),
            patch("app.services.gemini_service.asyncio.wait_for", side_effect=fake_wait_for),
        ):
            run_async(service.generate_structured_content("prompt", SampleStructuredResponse))

        call_kwargs = client.aio.models.generate_content.await_args.kwargs
        self.assertEqual(call_kwargs["model"], "test-model")
        self.assertEqual(captured_timeout, 12)

    def test_missing_api_key_raises_configuration_error(self):
        settings.gemini_api_key = ""
        service = GeminiService()

        with self.assertRaises(GeminiConfigurationError):
            run_async(service.generate_structured_content("prompt", SampleStructuredResponse))

    def test_timeout_maps_to_gemini_timeout_error(self):
        client = FakeGeminiClient({"value": "ok"})
        service = GeminiService()

        async def fake_timeout(awaitable, timeout):
            awaitable.close()
            raise asyncio.TimeoutError()

        with (
            patch("app.services.gemini_service.genai.Client", return_value=client),
            patch(
                "app.services.gemini_service.asyncio.wait_for",
                side_effect=fake_timeout,
            ),
        ):
            with self.assertRaises(GeminiTimeoutError):
                run_async(
                    service.generate_structured_content("prompt", SampleStructuredResponse)
                )

    def test_invalid_structured_response_maps_to_invalid_response_error(self):
        client = FakeGeminiClient({"unexpected": "shape"})
        service = GeminiService()

        with patch("app.services.gemini_service.genai.Client", return_value=client):
            with self.assertRaises(GeminiInvalidResponseError):
                run_async(
                    service.generate_structured_content("prompt", SampleStructuredResponse)
                )

    def test_upstream_sdk_failure_maps_to_upstream_error(self):
        class FakeAPIError(Exception):
            code = 500
            status = "INTERNAL"

        client = FakeGeminiClient({"value": "ok"})
        client.aio.models.generate_content = AsyncMock(side_effect=FakeAPIError("boom"))
        service = GeminiService()

        with (
            patch("app.services.gemini_service.genai.Client", return_value=client),
            patch("app.services.gemini_service.errors.APIError", FakeAPIError),
        ):
            with self.assertRaises(GeminiUpstreamError):
                run_async(
                    service.generate_structured_content("prompt", SampleStructuredResponse)
                )

    def test_generate_notes_content_regression_behavior_is_preserved(self):
        parsed_notes = GeneratedNotesContent(
            title="Title",
            table_of_contents=[],
            sections=[],
            summary="Summary",
            key_takeaways=["One"],
            one_minute_revision="Review",
        )
        service = GeminiService()

        with patch.object(
            service,
            "generate_structured_content",
            new=AsyncMock(return_value=parsed_notes),
        ) as mocked_helper:
            result = run_async(service.generate_notes_content("prompt"))

        self.assertIs(result, parsed_notes)
        mocked_helper.assert_awaited_once_with("prompt", GeneratedNotesContent)


if __name__ == "__main__":
    unittest.main()
