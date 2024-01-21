"""CRUD музыки"""
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status

from app.api.annotations import ProjectAnnotation
from app.api.dependencies.core import DBSessionDep
from app.api.schemas import MusicOut, ProjectOut
from app.models import MusicModel
from app.status_codes import MUSIC_NOT_FOUND, PROJECT_NOT_FOUND

router = APIRouter()


@router.post("/{project_id}", summary="Загрузить музыку в проект", responses=PROJECT_NOT_FOUND)
async def upload_music(
    project: ProjectAnnotation,
    music: Annotated[UploadFile, File(description="Файл музыки")],
    db_session: DBSessionDep,
) -> MusicOut:
    """Загрузка музыки в проект"""
    url = "https://lyrics-ide.storage.yandexcloud.net/beat_stub.mp3"
    duration_seconds = 184
    bpm = 90

    if project.music is not None:
        await db_session.delete(project.music)

    project.music = MusicModel(
        url=url,
        duration_seconds=duration_seconds,
        bpm=bpm,
    )
    await db_session.commit()

    return MusicOut(
        url=url,
        duration_seconds=duration_seconds,
        bpm=bpm,
    )


@router.get("/{project_id}", summary="Получить музыку проекта", responses={**PROJECT_NOT_FOUND, **MUSIC_NOT_FOUND})
async def get_music(project: ProjectAnnotation, db_session: DBSessionDep) -> MusicOut:
    """Получение музыки проекта"""
    if project.music is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Музыка не найдена")

    return MusicOut(
        url=project.music.url,
        duration_seconds=project.music.duration_seconds,
        bpm=project.music.bpm,
        custom_bpm=project.music.custom_bpm,
    )


@router.patch("/{project_id}", summary="Изменить BPM у музыки", responses={**PROJECT_NOT_FOUND, **MUSIC_NOT_FOUND})
async def set_music_bpm(
    project: ProjectAnnotation,
    custom_bpm: Annotated[int, Query(description="Пользовательское значение BPM", gt=0)],
    db_session: DBSessionDep,
) -> MusicOut:
    """Изменение пользовательского BPM у музыки"""
    if project.music is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Музыка не найдена")

    # Update the custom_bpm attribute of the music object
    project.music.custom_bpm = custom_bpm

    # Add the updated music object to the session and commit the changes
    db_session.add(project.music)

    # Return the updated music object
    new_music = MusicOut(
        url=project.music.url,
        duration_seconds=project.music.duration_seconds,
        bpm=project.music.bpm,
        custom_bpm=project.music.custom_bpm,
    )
    await db_session.commit()
    return new_music


@router.delete("/{project_id}", summary="Удалить музыку из проекта", responses={**PROJECT_NOT_FOUND, **MUSIC_NOT_FOUND})
async def delete_music(project: ProjectAnnotation, db_session: DBSessionDep) -> ProjectOut:
    """Удаление музыки из проекта"""
    if project.music is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Музыка не найдена")

    await db_session.delete(project.music)

    project_state = ProjectOut(
        name=project.name,
        description=project.description,
        project_id=project.project_id,
        texts=[],
        music=None,
    )

    await db_session.commit()

    return project_state
