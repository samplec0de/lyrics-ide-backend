"""Утилиты для работы со словами"""
import enum

import aiohttp
import pymorphy3
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import WordMeaningModel


morph = pymorphy3.MorphAnalyzer()


class WordMeaningSource(str, enum.Enum):
    """Источники значений слова"""

    OJEGOV = "Ojegov"


def get_word_normal_forms(word: str) -> set[str]:
    """Приведение слова к нормальной форме.
    Так как вариантов может быть несколько в зависимости от значения, возвращается множество."""
    parsing_result = morph.parse(word)
    if parsing_result:
        normal_forms = {word_variant.normal_form for word_variant in parsing_result}
    else:
        normal_forms = {word}
    return normal_forms


async def get_word_meanings(word: str, db_session: AsyncSession) -> list[str]:
    """Получить значения всех нормальных форм слова"""
    normal_forms = get_word_normal_forms(word)

    word_meaning_query = select(WordMeaningModel).where(
        WordMeaningModel.word.in_([form.lower().capitalize() for form in normal_forms])
    )
    word_meaning_results = await db_session.execute(word_meaning_query)
    word_meanings = [word_meaning.meaning for word_meaning in word_meaning_results.scalars()]

    return word_meanings


async def get_synonyms(word: str) -> list[str]:
    """Получить синонимы к слову"""
    endpoint = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"
    params = {"key": settings.yandex_dict_key, "lang": "ru-ru", "text": word}
    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, data=params) as response:
            if response.status != 200:
                return []
            lookup_result = await response.json()
            synonyms = []
            for definition in lookup_result["def"]:
                for synonym in definition.get("tr", []):
                    synonyms.append(synonym["text"])
            return synonyms
