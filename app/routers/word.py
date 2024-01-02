from typing import Annotated

from fastapi import APIRouter, status, Query

from app.annotations import WordAnnotation, UserAnnotation
from app.schemas import WordMeaning
from app.status_codes import MEANING_NOT_FOUND

router = APIRouter()


@router.get(
    "/meaning",
    summary="Получить значение слова",
    responses=MEANING_NOT_FOUND
)
async def get_text(current_user: UserAnnotation, word: WordAnnotation) -> WordMeaning:
    return WordMeaning(meaning="значение слова", source="GRAND_DICTIONARY")


@router.get(
    "/synonyms",
    summary="Получить синонимы к слову"
)
async def get_text(current_user: UserAnnotation, word: WordAnnotation) -> list[str]:
    return ["синоним 1", "синоним 2", "синоним 3"]


@router.get(
    "/rhyming",
    summary="Получить рифмующиеся слова к слову"
)
async def get_text(current_user: UserAnnotation, word: WordAnnotation) -> list[str]:
    return ["рифма 1", "рифма 2"]
