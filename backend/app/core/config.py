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

    # Comma-separated list of allowed CORS origins.
    # Supports localhost development and Vercel deployments.
    cors_allowed_origins: str = "http://127.0.0.1:5500,http://localhost:5500,http://127.0.0.1:8080,http://localhost:8080,http://127.0.0.1:3000,http://localhost:3000"

    @property
    def get_cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]

    # Gemini settings. The API key is optional at startup so /health keeps
    # working in local environments before notes generation is configured.
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.1-flash-lite"
    gemini_timeout_seconds: float = 30.0

    # DeepSeek settings
    deepseek_api_key: str | None = None
    deepseek_model: str = "deepseek-chat"

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
