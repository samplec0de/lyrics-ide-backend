"""Эндпоинты для получения мета информации о словах"""
from fastapi import APIRouter

from app.api.annotations import UserAnnotation, WordAnnotation
from app.api.dependencies.core import DBSessionDep
from app.api.schemas import WordMeaning
from app.status_codes import MEANING_NOT_FOUND
from app.word_utils import WordMeaningSource
from app.word_utils import get_synonyms as get_synonyms_utils
from app.word_utils import get_word_meanings as get_word_meanings_utils

router = APIRouter()


@router.get("/meaning", summary="Получить значение слова", responses=MEANING_NOT_FOUND)
async def get_meanings(
    current_user: UserAnnotation, word: WordAnnotation, db_session: DBSessionDep
) -> list[WordMeaning]:
    """Получить значение слова"""
    meanings = await get_word_meanings_utils(word=word, db_session=db_session)
    return [WordMeaning(meaning=meaning, source=WordMeaningSource.OJEGOV) for meaning in meanings]


@router.get("/synonyms", summary="Получить синонимы к слову")
async def get_synonyms(current_user: UserAnnotation, word: WordAnnotation) -> list[str]:
    """Получить синонимы к слову"""
    return await get_synonyms_utils(word=word)


@router.get("/rhyming", summary="Получить рифмующиеся слова к слову")
async def get_rhyming(current_user: UserAnnotation, word: WordAnnotation) -> list[str]:
    """Получить рифмующиеся слова к слову"""
    return ["рифма 1", "рифма 2"]
