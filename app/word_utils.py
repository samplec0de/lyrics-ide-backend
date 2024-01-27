import enum

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import WordMeaningModel


class WordMeaningSource(str, enum.Enum):
    OJEGOV = "Ojegov"


async def get_word_meanings(word: str, db_session: AsyncSession) -> list[str]:
    """Получить значения слова"""
    word_meaning_query = select(WordMeaningModel).where(WordMeaningModel.word == word.lower().capitalize())
    word_meaning_results = await db_session.execute(word_meaning_query)
    word_meanings = [word_meaning.meaning for word_meaning in word_meaning_results.scalars()]
    return word_meanings
