"""Internal Gemini service errors with sanitized API mappings."""


class GeminiConfigurationError(Exception):
    """Gemini is not configured correctly for the requested operation."""


class GeminiTimeoutError(Exception):
    """Gemini did not return a response within the configured timeout."""


class GeminiUpstreamError(Exception):
    """Gemini returned an upstream failure or the SDK call failed."""


class GeminiInvalidResponseError(Exception):
    """Gemini returned content that could not be validated safely."""
