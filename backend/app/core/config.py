"""
Application configuration.

Settings are loaded from environment variables, with a local `.env` file
(not committed to Git) used for local development overrides.

Milestone 1 scope only: application identity, environment name, and the
allowed frontend origin for CORS. Gemini-related settings will be added
when Gemini integration begins (a later milestone), per PROJECT_CONTEXT.md
section 24 and the Milestone 1 task instructions.
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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Single shared settings instance, imported wherever configuration is needed.
settings = Settings()
