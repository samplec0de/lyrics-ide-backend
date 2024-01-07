from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends

from app.api.annotations import ProjectAnnotation, UserAnnotation
from app.database_dumb import projects
from app.api.routers.dependencies import get_project_by_id
from app.api.schemas import ProjectOut, ProjectIn
from app.status_codes import PROJECT_NOT_FOUND

router = APIRouter()


@router.post("/", summary="Создать проект")
async def create_project(current_user: UserAnnotation, project: ProjectIn) -> ProjectOut:
    project_id = uuid4()
    projects[project_id] = ProjectOut(**project.model_dump(), id=project_id)
    return projects[project_id]


@router.get("/", summary="Получить список проектов")
async def get_projects(current_user: UserAnnotation) -> list[ProjectOut]:
    return list(projects.values())


@router.get(
    "/{project_id}",
    summary="Получить содержимое проекта",
    responses=PROJECT_NOT_FOUND
)
async def get_project(current_user: UserAnnotation, project: ProjectAnnotation) -> ProjectOut:
    return project


@router.delete("/{project_id}", summary="Удалить проект")
async def delete_project(current_user: UserAnnotation, project: ProjectAnnotation):
    projects.pop(project.id)
