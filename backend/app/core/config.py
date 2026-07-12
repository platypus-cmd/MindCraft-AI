"""
Application configuration.

Settings are loaded from environment variables, with a local `.env` file
(not committed to Git) used for local development overrides.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application identity
    app_name: str = "MindCraft AI"
    api_version: str = "v1"

    # Environment: "development" or "production"
    environment: str = "development"

    # Local frontend origin, used for CORS in development.
    # Default matches the built-in static server documented in the README:
    #   python -m http.server 5500 --directory frontend
    frontend_origin: str = "http://127.0.0.1:5500"

    # Gemini settings. The API key is optional at startup so /health keeps
    # working in local environments before notes generation is configured.
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"
    gemini_timeout_seconds: float = 30.0

    # Document (PDF) upload settings. See PROJECT_CONTEXT.md Section 22
    # ("enforce reasonable limits on...PDF file size").
    max_pdf_size_bytes: int = 10 * 1024 * 1024  # 10 MB

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Single shared settings instance, imported wherever configuration is needed.
settings = Settings()
