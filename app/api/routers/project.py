"""CRUD проектов"""
from uuid import uuid4

from fastapi import APIRouter

from app.api.annotations import ProjectAnnotation, UserAnnotation
from app.api.schemas import ProjectIn, ProjectOut
from app.database_dumb import projects
from app.status_codes import PROJECT_NOT_FOUND

router = APIRouter()


@router.post("/", summary="Создать проект")
async def create_project(current_user: UserAnnotation, project: ProjectIn) -> ProjectOut:
    """Создать проект"""
    project_id = uuid4()
    projects[project_id] = ProjectOut(**project.model_dump(), id=project_id)
    return projects[project_id]


@router.get("/", summary="Получить список проектов")
async def get_projects(current_user: UserAnnotation) -> list[ProjectOut]:
    """Получить список проектов"""
    return list(projects.values())


@router.get("/{project_id}", summary="Получить содержимое проекта", responses=PROJECT_NOT_FOUND)
async def get_project(current_user: UserAnnotation, project: ProjectAnnotation) -> ProjectOut:
    """Получить содержимое проекта"""
    return project


@router.delete("/{project_id}", summary="Удалить проект")
async def delete_project(current_user: UserAnnotation, project: ProjectAnnotation):
    """Удалить проект"""
    projects.pop(project.id)
