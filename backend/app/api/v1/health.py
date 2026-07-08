"""
Health check endpoint.

Used to verify that the backend service is running and reachable from the
frontend. No business logic lives here; this route only reports status.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    """Response model for GET /api/v1/health."""

    app_name: str
    status: str
    api_version: str


@router.get("/health", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    """Return basic service status information."""
    return HealthResponse(
        app_name=settings.app_name,
        status="ok",
        api_version=settings.api_version,
    )
