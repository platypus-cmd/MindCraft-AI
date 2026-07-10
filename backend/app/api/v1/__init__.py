"""
Aggregates all /api/v1 routes into a single router.

As new resource routers are added in later milestones (notes, flashcards,
quizzes, revision, documents), they should be imported and included here
so app/main.py only ever needs to include one v1 router.
"""

from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.notes import router as notes_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(health_router, tags=["health"])
api_v1_router.include_router(notes_router, tags=["notes"])
