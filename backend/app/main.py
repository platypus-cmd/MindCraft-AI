"""
FastAPI application entry point.

Run locally with (from the backend/ directory, virtual environment active):
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_v1_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

# CORS: only allow the configured local frontend origin.
# Section 30 (Security Requirements) requires CORS to be configured only
# for required origins, not left open.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)
