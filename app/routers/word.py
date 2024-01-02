from typing import Annotated

from fastapi import APIRouter, status, Query

from app.schemas import WordMeaning

router = APIRouter()

WordAnnotation = Annotated[str, Query(description="слово", min_length=3, max_length=33)]
MEANING_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "Не найдено значение слова"}}


@router.get(
    "/meaning",
    summary="Получить значение слова",
    responses=MEANING_NOT_FOUND
)
async def get_text(word: WordAnnotation) -> WordMeaning:
    return WordMeaning(meaning="значение слова", source="GRAND_DICTIONARY")


@router.get(
    "/synonyms",
    summary="Получить синонимы к слову"
)
async def get_text(word: WordAnnotation) -> list[str]:
    return ["синоним 1", "синоним 2", "синоним 3"]


@router.get(
    "/rhyming",
    summary="Получить рифмующиеся слова к слову"
)
async def get_text(word: WordAnnotation) -> list[str]:
    return ["рифма 1", "рифма 2"]
