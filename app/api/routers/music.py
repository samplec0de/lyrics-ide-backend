"""CRUD музыки"""
from tempfile import NamedTemporaryFile
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status

from app.api.annotations import CurrentUserAnnotation, OwnOrGrantProjectAnnotation, OwnProjectAnnotation
from app.api.dependencies.core import DBSessionDep
from app.api.schemas import MusicOut, ProjectOut, TextVariantCompact
from app.grant_utils import get_grant_level_by_user_and_project
from app.models import MusicModel
from app.music_utils import get_file_bpm, get_song_duration
from app.s3_helpers import delete, generate_presigned_url, upload
from app.status_codes import MUSIC_NOT_FOUND, PROJECT_NOT_FOUND

router = APIRouter()


@router.post(
    "/{project_id}",
    summary="Загрузить музыку в проект",
    responses=PROJECT_NOT_FOUND,
    operation_id="upload_music",
)
async def upload_music(
    project: OwnProjectAnnotation,
    music: Annotated[UploadFile, File(description="Файл музыки")],
    db_session: DBSessionDep,
) -> MusicOut:
    """Загрузка музыки в проект"""

    if music.filename is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Файл не найден")

    with NamedTemporaryFile(suffix=f"{music.filename[music.filename.rindex('.'):]}") as temp_file:
        temp_file_path = temp_file.name
        music_content = await music.read()
        temp_file.write(music_content)
        temp_file.flush()

        duration_seconds = await get_song_duration(temp_file_path)
        bpm = int(await get_file_bpm(temp_file_path) or -1)

    project_id = project.project_id

    if project.music is not None:
        await delete(project.music.url)
        await db_session.delete(project.music)
        await db_session.commit()
        await db_session.refresh(project)

    key = f"{project_id}/music/{music.filename}"
    await upload(
        key=key,
        bytes_data=music_content,
    )

    project.music = MusicModel(
        url=key,
        duration_seconds=duration_seconds or -1,
        bpm=bpm,
    )
    await db_session.commit()

    url = await generate_presigned_url(key)

    return MusicOut(
        url=url,
        duration_seconds=duration_seconds or -1,
        bpm=bpm,
    )


@router.get(
    "/{project_id}",
    summary="Получить музыку проекта",
    responses={**PROJECT_NOT_FOUND, **MUSIC_NOT_FOUND},
    operation_id="get_music",
)
async def get_music(project: OwnOrGrantProjectAnnotation) -> MusicOut:
    """Получение музыки проекта"""
    if project.music is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Музыка не найдена")

    url = await generate_presigned_url(project.music.url)

    return MusicOut(
        url=url,
        duration_seconds=project.music.duration_seconds,
        bpm=project.music.bpm,
        custom_bpm=project.music.custom_bpm,
    )


@router.patch(
    "/{project_id}",
    summary="Изменить BPM у музыки",
    responses={**PROJECT_NOT_FOUND, **MUSIC_NOT_FOUND},
    operation_id="set_music_bpm",
)
async def set_music_bpm(
    project: OwnProjectAnnotation,
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

    url = await generate_presigned_url(project.music.url)

    # Return the updated music object
    new_music = MusicOut(
        url=url,
        duration_seconds=project.music.duration_seconds,
        bpm=project.music.bpm,
        custom_bpm=project.music.custom_bpm,
    )
    await db_session.commit()
    return new_music


@router.delete(
    "/{project_id}",
    summary="Удалить музыку из проекта",
    responses={**PROJECT_NOT_FOUND, **MUSIC_NOT_FOUND},
    operation_id="delete_music",
)
async def delete_music(
    project: OwnProjectAnnotation, current_user: CurrentUserAnnotation, db_session: DBSessionDep
) -> ProjectOut:
    """Удаление музыки из проекта"""
    if project.music is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Музыка не найдена")

    await delete(project.music.url)

    await db_session.delete(project.music)
    await db_session.commit()
    await db_session.refresh(project)

    user_grant_level = await get_grant_level_by_user_and_project(
        user_id=current_user.user_id, project_id=project.project_id, db_session=db_session
    )

    project_state = ProjectOut(
        name=project.name,
        description=project.description,
        project_id=project.project_id,
        owner_user_id=project.owner_user_id,
        is_owner=project.owner_user_id == current_user.user_id,
        grant_level=user_grant_level,
        texts=[
            TextVariantCompact(
                text_id=text.text_id,
                name=text.name,
                created_at=text.created_at,
                updated_at=text.updated_at,
            )
            for text in project.texts
        ],
        music=None,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )

    return project_state
