"""Утилиты для работы со словами"""
import enum

import aiohttp
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import WordMeaningModel


class WordMeaningSource(str, enum.Enum):
    """Источники значений слова"""

    OJEGOV = "Ojegov"


async def get_word_meanings(word: str, db_session: AsyncSession) -> list[str]:
    """Получить значения слова"""
    word_meaning_query = select(WordMeaningModel).where(WordMeaningModel.word == word.lower().capitalize())
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
