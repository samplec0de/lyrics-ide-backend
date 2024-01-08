"""Pydantic схемы для валидации данных в API"""
from typing import Annotated
from uuid import UUID

from fastapi import UploadFile
from pydantic import UUID4, BaseModel, Field


class TextVariantBase(BaseModel):
    """Базовая схема для варианта текста"""

    name: Annotated[str | None, Field(description="Название варианта текста")] = None


class TextVariantIn(TextVariantBase):
    """Схема для варианта текста при создании"""

    project_id: Annotated[UUID4, Field(description="Идентификатор проекта")]


class TextVariantCompact(TextVariantBase):
    """Схема для варианта текста при отображении в списке проектов"""

    id: Annotated[UUID4, Field(description="Идентификатор варианта текста")]


class TextVariant(TextVariantCompact):
    """Полная схема для варианта текста для получения проекта"""

    text: Annotated[str, Field(description="Текст")]


class TextVariantWithoutID(TextVariantBase):
    """Схема для варианта текста для изменения"""

    text: Annotated[str, Field(description="Текст")]


class MusicBase(BaseModel):
    """Базовая схема для музыки"""


class MusicIn(MusicBase):
    """Схема для музыки при создании"""

    file: Annotated[UploadFile | None, Field(description="Файл музыки")] = None


class MusicOut(MusicBase):
    """Полная схема музыки для отображения"""

    url: Annotated[str, Field(description="Ссылка на музыку (s3 pre-signed URL)")]
    duration_seconds: Annotated[int, Field(description="Длительность музыки в секундах")]
    bpm: Annotated[int, Field(description="BPM музыки определенный автоматически")]
    custom_bpm: Annotated[int | None, Field(description="BPM музыки установленный пользователем")] = None


class ProjectBase(BaseModel):
    """Базовая схема для проекта"""

    name: Annotated[str | None, Field(description="Название проекта")] = None
    description: Annotated[str | None, Field(description="Описание проекта")] = None


class ProjectIn(ProjectBase):
    """Схема для проекта при создании"""

    texts: Annotated[list[TextVariant], Field(description="Варианты текста")] = []
    music: Annotated[MusicIn | None, Field(description="Музыкальный трек")] = None


class ProjectOut(ProjectBase):
    """Полная схема для проекта для отображения"""

    id: Annotated[UUID4, Field(description="Идентификатор проекта")]
    texts: Annotated[list[TextVariantCompact], Field(description="Варианты текста")] = []
    music: Annotated[MusicOut | None, Field(description="Музыкальный трек")] = None


class WordMeaning(BaseModel):
    """Схема для отображения значения слова"""

    meaning: Annotated[str, Field(description="Значение слова")]
    source: Annotated[str, Field(description="Источник значения слова")]


if __name__ == "__main__":
    print(TextVariant(id=UUID("fa576398-f5d2-436d-913c-23b33681f03b"), name="Test", text="text"))
