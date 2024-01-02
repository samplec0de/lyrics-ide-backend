from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Query, HTTPException, status

from app.annotations import ProjectAnnotation
from app.status_codes import PROJECT_NOT_FOUND

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
    responses={
        **PROJECT_NOT_FOUND,
        status.HTTP_400_BAD_REQUEST: {
            "description": "Нельзя поменять BPM у проекта без музыки"
        }
    }
)
async def set_music_bpm(
        project: ProjectAnnotation,
        custom_bpm: Annotated[int, Query(description="Пользовательское значение BPM", gt=0)]
):
    if project.music is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нельзя поменять BPM у проекта без музыки")

    project.music.custom_bpm = custom_bpm
