"""Focused revision orchestration service."""

from app.prompts.revision import build_revision_prompt
from app.schemas.revision import RevisionRequest, RevisionResponse
from app.services.gemini_service import gemini_service


async def generate_revision(request: RevisionRequest) -> RevisionResponse:
    prompt = build_revision_prompt(request)
    return await gemini_service.generate_structured_content(prompt, RevisionResponse)

