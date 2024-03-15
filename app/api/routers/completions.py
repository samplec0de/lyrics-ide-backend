"""Прокси над LLM для автодополнения"""
from fastapi import APIRouter

from app.api.schemas import CompletionIn, CompletionOut
from app.llm import get_llm_lyrics_completions

router = APIRouter()


@router.post(
    "/",
    summary="Продолжить текст",
    operation_id="create_completion",
)
async def create_completion(completion_input: CompletionIn) -> list[CompletionOut]:
    """Продолжить текст"""
    completions = get_llm_lyrics_completions(completion_input.text)
    return [CompletionOut(completion=completion) for completion in completions]
