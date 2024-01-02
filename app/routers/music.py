from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Query, HTTPException, status

from app.annotations import ProjectAnnotation
from app.schemas import MusicOut
from app.status_codes import PROJECT_NOT_FOUND, MUSIC_NOT_FOUND

router = APIRouter()


@router.post(
    "/music/{project_id}", summary="Загрузить музыку в проект",
    responses=PROJECT_NOT_FOUND
)
async def set_music(
        project: ProjectAnnotation,
        music: Annotated[UploadFile, File(description="Файл музыки")]
):
    project.music.url = "https://lyrics-ide.storage.yandexcloud.net/beat_stub.mp3"


@router.patch(
    "/music/{project_id}",
    summary="Изменить BPM у музыки",
    responses={**PROJECT_NOT_FOUND, **MUSIC_NOT_FOUND}
)
async def set_music_bpm(
        project: ProjectAnnotation,
        custom_bpm: Annotated[int, Query(description="Пользовательское значение BPM", gt=0)]
):
    if project.music is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Музыка не найдена")

    project.music.custom_bpm = custom_bpm


@router.delete(
    "/music/{project_id}",
    summary="Удалить музыку из проекта",
    responses={**PROJECT_NOT_FOUND, **MUSIC_NOT_FOUND}
)
async def delete_music(project: ProjectAnnotation):
    if project.music is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Музыка не найдена")

    project.music = None


@router.get(
    "/music/{project_id}",
    summary="Получить музыку проекта",
    responses={**PROJECT_NOT_FOUND, **MUSIC_NOT_FOUND}
)
async def get_music(project: ProjectAnnotation) -> MusicOut:
    if project.music is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Музыка не найдена")

    return project.music
