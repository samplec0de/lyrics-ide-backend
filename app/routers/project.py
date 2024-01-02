from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, UploadFile, HTTPException, status, Depends, File, Query

from app.database import projects
from app.routers.dependencies import get_project_by_id
from app.schemas import ProjectOut, ProjectIn

router = APIRouter()

ProjectAnnotation = Annotated[ProjectOut, Depends(get_project_by_id)]
PROJECT_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "Проект с заданным id не существует"}}


@router.get("/", summary="Получить список проектов")
async def get_projects() -> list[ProjectOut]:
    return list(projects.values())


@router.get(
    "/{project_id}",
    summary="Получить содержимое проекта",
    responses=PROJECT_NOT_FOUND
)
async def get_project(project: ProjectAnnotation) -> ProjectOut:
    return project


@router.post("/", summary="Создать проект")
async def create_project(project: ProjectIn) -> ProjectOut:
    project_id = uuid4()
    projects[project_id] = ProjectOut(**project.model_dump(), id=project_id)
    return projects[project_id]


@router.delete("/{project_id}", summary="Удалить проект")
async def delete_project(project: ProjectAnnotation):
    projects.pop(project.id)


@router.post(
    "/{project_id}/music", summary="Загрузить музыку в проект",
    responses=PROJECT_NOT_FOUND
)
async def set_music(
        project: ProjectAnnotation,
        music: Annotated[UploadFile, File(description="Файл музыки")]
):
    project.music.url = "https://lyrics-ide.storage.yandexcloud.net/beat_stub.mp3"


@router.patch(
    "/{project_id}/music",
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
