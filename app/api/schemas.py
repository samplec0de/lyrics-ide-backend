"""Pydantic схемы для валидации данных в API"""
import datetime
from typing import Annotated

from fastapi import UploadFile
from pydantic import UUID4, BaseModel, Field

from app.models.grant import GrantLevel


class TextVariantBase(BaseModel):
    """Базовая схема для варианта текста"""

    name: Annotated[str | None, Field(description="Название варианта текста")] = None


class TextVariantIn(TextVariantBase):
    """Схема для варианта текста при создании"""

    project_id: Annotated[UUID4, Field(description="Идентификатор проекта")]


class TextVariantCompact(TextVariantBase):
    """Схема для варианта текста при отображении в списке проектов"""

    text_id: Annotated[UUID4, Field(description="Идентификатор варианта текста")]
    created_at: Annotated[datetime.datetime, Field(description="Дата создания проекта")]
    updated_at: Annotated[datetime.datetime, Field(description="Дата последнего обновления проекта")]


class TextVariant(TextVariantCompact):
    """Полная схема для варианта текста для получения проекта"""

    payload: Annotated[dict, Field(description="JSON с текстом")]


class TextVariantWithoutID(TextVariantBase):
    """Схема для варианта текста для изменения"""

    payload: Annotated[dict | None, Field(description="JSON с текстом")] = None


class MusicBase(BaseModel):
    """Базовая схема для музыки"""


class MusicIn(MusicBase):
    """Схема для музыки при создании"""

    file: Annotated[UploadFile | None, Field(description="Файл музыки")] = None


class MusicOut(MusicBase):
    """Полная схема музыки для отображения"""

    url: Annotated[str, Field(description="Ссылка на музыку (s3 pre-signed URL)")]
    duration_seconds: Annotated[float, Field(description="Длительность музыки в секундах")]
    bpm: Annotated[int | None, Field(description="BPM музыки определенный автоматически")]
    custom_bpm: Annotated[int | None, Field(description="BPM музыки установленный пользователем")] = None


class ProjectBase(BaseModel):
    """Базовая схема для проекта"""

    name: Annotated[str | None, Field(description="Название проекта")] = None
    description: Annotated[str | None, Field(description="Описание проекта")] = None


class ProjectIn(ProjectBase):
    """Схема для проекта при создании"""

    texts: Annotated[list[TextVariant] | None, Field(description="Варианты текста")] = []
    music: Annotated[MusicIn | None, Field(description="Музыкальный трек")] = None


class ProjectOut(ProjectBase):
    """Полная схема для проекта для отображения"""

    project_id: Annotated[UUID4, Field(description="Идентификатор проекта")]
    owner_user_id: Annotated[UUID4, Field(description="Идентификатор пользователя-владельца проекта")]
    is_owner: Annotated[bool, Field(description="Является ли текущий пользователь владельцем проекта")]
    created_at: Annotated[datetime.datetime, Field(description="Дата создания проекта")]
    updated_at: Annotated[datetime.datetime, Field(description="Дата последнего обновления проекта")]
    texts: Annotated[list[TextVariantCompact], Field(description="Варианты текста")] = []
    music: Annotated[MusicOut | None, Field(description="Музыкальный трек")] = None


class WordMeaning(BaseModel):
    """Схема для отображения значения слова"""

    meaning: Annotated[str, Field(description="Значение слова")]
    source: Annotated[str, Field(description="Источник значения слова")]


class CompletionIn(BaseModel):
    """Схема куска текста для автодополнения"""

    text: str


class CompletionOut(BaseModel):
    """Схема для варианта результата автодополнения текста"""

    completion: Annotated[str, Field(description="Продолжение текста")]


class ProjectGrantCode(BaseModel):
    """Схема для кода доступа к проекту"""

    grant_code_id: Annotated[UUID4, Field(description="Код доступа к проекту")]
    project_id: Annotated[UUID4, Field(description="Идентификатор проекта")]
    issuer_user_id: Annotated[UUID4, Field(description="Идентификатор пользователя, создавшего код доступа")]
    level: Annotated[GrantLevel, Field(description="Уровень доступа к проекту")]
    max_activations: Annotated[int, Field(description="Максимальное количество активаций кода")]
    current_activations: Annotated[int, Field(description="Количество активаций кода")]
    is_active: Annotated[bool, Field(description="Активен ли код доступа к проекту")]
    created_at: Annotated[datetime.datetime, Field(description="Дата создания кода")]
    updated_at: Annotated[datetime.datetime, Field(description="Дата последнего обновления кода")]


class ProjectGrant(BaseModel):
    """Схема для гранта доступа к проекту"""

    project_id: Annotated[UUID4, Field(description="Идентификатор проекта")]
    user_id: Annotated[UUID4, Field(description="Идентификатор пользователя")]
    user_email: Annotated[str, Field(description="Email пользователя")]
    level: Annotated[GrantLevel, Field(description="Уровень доступа к проекту")]
    created_at: Annotated[datetime.datetime, Field(description="Дата создания гранта")]
