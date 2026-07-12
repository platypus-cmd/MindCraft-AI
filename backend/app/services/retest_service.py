"""Targeted retest orchestration and deterministic validation."""

from app.prompts.retest import build_retest_prompt
from app.schemas.quiz import QuizResponse
from app.schemas.retest import RetestRequest
from app.services.gemini_errors import GeminiInvalidResponseError
from app.services.gemini_service import gemini_service

MIN_RETEST_QUESTIONS = 5
MAX_RETEST_QUESTIONS = 8


def normalize_for_comparison(value: str) -> str:
    return " ".join(value.strip().split()).casefold()


def select_retest_question_count(weak_concepts: list[str]) -> int:
    if len(weak_concepts) <= 2:
        return MIN_RETEST_QUESTIONS
    return MAX_RETEST_QUESTIONS


async def generate_retest(request: RetestRequest) -> QuizResponse:
    target_count = select_retest_question_count(request.weak_concepts)
    prompt = build_retest_prompt(request, target_count)
    response = await gemini_service.generate_structured_content(prompt, QuizResponse)
    validate_retest_response(response, request, target_count)
    return response


def validate_retest_response(
    response: QuizResponse,
    request: RetestRequest,
    target_count: int,
) -> None:
    if len(response.questions) != target_count:
        raise GeminiInvalidResponseError("Retest question count did not match target.")

    allowed_concepts = {
        normalize_for_comparison(concept)
        for concept in request.weak_concepts
    }
    original_questions = {
        normalize_for_comparison(question)
        for question in request.original_questions
    }
    generated_questions: set[str] = set()

    for question in response.questions:
        concept_key = normalize_for_comparison(question.concept)
        if concept_key not in allowed_concepts:
            raise GeminiInvalidResponseError("Retest question concept was not requested.")

        question_key = normalize_for_comparison(question.question)
        if question_key in original_questions:
            raise GeminiInvalidResponseError("Retest repeated an original question.")

        if question_key in generated_questions:
            raise GeminiInvalidResponseError("Retest contained duplicate questions.")

        generated_questions.add(question_key)

