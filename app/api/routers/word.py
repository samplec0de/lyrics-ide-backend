"""Эндпоинты для получения мета информации о словах"""
from fastapi import APIRouter

from app.api.annotations import UserAnnotation, WordAnnotation
from app.api.schemas import WordMeaning
from app.status_codes import MEANING_NOT_FOUND

router = APIRouter()


@router.get("/meaning", summary="Получить значение слова", responses=MEANING_NOT_FOUND)
async def get_meaning(current_user: UserAnnotation, word: WordAnnotation) -> WordMeaning:
    """Получить значение слова"""
    return WordMeaning(meaning="значение слова", source="GRAND_DICTIONARY")


@router.get("/synonyms", summary="Получить синонимы к слову")
async def get_synonyms(current_user: UserAnnotation, word: WordAnnotation) -> list[str]:
    """Получить синонимы к слову"""
    return ["синоним 1", "синоним 2", "синоним 3"]


@router.get("/rhyming", summary="Получить рифмующиеся слова к слову")
async def get_rhyming(current_user: UserAnnotation, word: WordAnnotation) -> list[str]:
    """Получить рифмующиеся слова к слову"""
    return ["рифма 1", "рифма 2"]
