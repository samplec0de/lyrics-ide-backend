"""CRUD музыки"""
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status

from app.api.annotations import ProjectAnnotation, UserAnnotation
from app.api.schemas import MusicOut
from app.status_codes import MUSIC_NOT_FOUND, PROJECT_NOT_FOUND

router = APIRouter()


@router.post("/{project_id}", summary="Загрузить музыку в проект", responses=PROJECT_NOT_FOUND)
async def upload_music(
    current_user: UserAnnotation,
    project: ProjectAnnotation,
    music: Annotated[UploadFile, File(description="Файл музыки")],
):
    """Загрузка музыки в проект"""
    project.music = MusicOut(
        url="https://lyrics-ide.storage.yandexcloud.net/beat_stub.mp3",
        duration_seconds=184,
        bpm=90,
    )


@router.get("/{project_id}", summary="Получить музыку проекта", responses={**PROJECT_NOT_FOUND, **MUSIC_NOT_FOUND})
async def get_music(current_user: UserAnnotation, project: ProjectAnnotation) -> MusicOut:
    """Получение музыки проекта"""
    if project.music is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Музыка не найдена")

    return project.music


@router.patch("/{project_id}", summary="Изменить BPM у музыки", responses={**PROJECT_NOT_FOUND, **MUSIC_NOT_FOUND})
async def set_music_bpm(
    current_user: UserAnnotation,
    project: ProjectAnnotation,
    custom_bpm: Annotated[int, Query(description="Пользовательское значение BPM", gt=0)],
):
    """Изменение пользовательского BPM у музыки"""
    if project.music is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Музыка не найдена")

    project.music.custom_bpm = custom_bpm


@router.delete("/{project_id}", summary="Удалить музыку из проекта", responses={**PROJECT_NOT_FOUND, **MUSIC_NOT_FOUND})
async def delete_music(project: ProjectAnnotation):
    """Удаление музыки из проекта"""
    if project.music is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Музыка не найдена")

    project.music = None
