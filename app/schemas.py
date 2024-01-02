from typing import Annotated

from fastapi import UploadFile
from pydantic import BaseModel, UUID4, Field


class TextVariantBase(BaseModel):
    name: Annotated[str, Field(description="Название варианта текста")] = None
    text: Annotated[str, Field(description="Текст")]


class TextVariantCompact(TextVariantBase):
    id: Annotated[UUID4, Field(description="Идентификатор варианта текста")]
    name: Annotated[str, Field(description="Название варианта текста")] = None


class MusicBase(BaseModel):
    pass


class MusicIn(MusicBase):
    file: Annotated[UploadFile, Field(description="Файл музыки")] = None


class MusicOut(MusicBase):
    url: Annotated[str, Field(description="Ссылка на музыку (s3 pre-signed URL)")] = None
    duration_seconds: Annotated[int, Field(description="Длительность музыки в секундах")]
    bpm: Annotated[int, Field(description="BPM музыки определенный автоматически")]
    custom_bpm: Annotated[int, Field(description="BPM музыки установленный пользователем")] = None


class ProjectBase(BaseModel):
    name: Annotated[str, Field(description="Название проекта")] = None
    description: Annotated[str, Field(description="Описание проекта")] = None
    texts: Annotated[list[TextVariant], Field(description="Варианты текста")] = []
    music: Annotated[MusicIn, Field(description="Музыкальный трек")] = None


class ProjectIn(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: Annotated[UUID4, Field(description="Идентификатор проекта")]
    texts: Annotated[list[TextVariantCompact], Field(description="Варианты текста")] = []
    music: Annotated[MusicOut, Field(description="Музыкальный трек")] = None
