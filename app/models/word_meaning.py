# pylint: disable=cyclic-import, unsubscriptable-object
"""ORM модель варианта значения слова"""
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class WordMeaningModel(Base):  # type: ignore
    """ORM модель варианта значения слова"""

    __tablename__ = "word_meaning"

    word_meaning_id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(index=True)
    meaning: Mapped[str]
    first_character: Mapped[str]
