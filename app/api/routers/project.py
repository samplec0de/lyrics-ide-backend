"""CRUD проектов"""
from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.annotations import ProjectAnnotation
from app.api.dependencies.core import DBSessionDep
from app.api.schemas import MusicOut, ProjectBase, ProjectOut, TextVariantCompact
from app.models import ProjectModel
from app.s3 import generate_presigned_url
from app.status_codes import PROJECT_NOT_FOUND

router = APIRouter()


# pylint: disable=fixme
@router.post("/", summary="Создать проект")
async def create_project(project: ProjectBase, db_session: DBSessionDep) -> ProjectOut:
    """Создать проект"""
    new_project = ProjectModel(name=project.name, description=project.description)

    db_session.add(new_project)
    await db_session.commit()
    await db_session.refresh(new_project)

    return ProjectOut(
        name=new_project.name,
        description=new_project.description,
        project_id=new_project.project_id,
        texts=[],
        music=None,
    )


@router.get("/", summary="Получить список проектов")
async def get_projects(db_session: DBSessionDep) -> list[ProjectOut]:
    """Получить список проектов"""
    result = await db_session.execute(
        select(ProjectModel).options(selectinload(ProjectModel.music), selectinload(ProjectModel.texts))
    )
    projects = result.scalars().all()

    return [
        ProjectOut(
            name=project.name,
            description=project.description,
            project_id=project.project_id,
            texts=[
                TextVariantCompact(
                    text_id=text.text_id,
                    name=text.name,
                )
                for text in project.texts
            ],
            music=MusicOut(
                url=await generate_presigned_url(project.music.url),
                duration_seconds=project.music.duration_seconds,
                bpm=project.music.bpm,
                custom_bpm=project.music.custom_bpm,
            )
            if project.music
            else None,
        )
        for project in projects
    ]


@router.get("/{project_id}", summary="Получить содержимое проекта", responses=PROJECT_NOT_FOUND)
async def get_project(project: ProjectAnnotation) -> ProjectOut:
    """Получить содержимое проекта"""
    music = project.music

    return ProjectOut(
        name=project.name,
        description=project.description,
        project_id=project.project_id,
        texts=[
            TextVariantCompact(
                text_id=text.text_id,
                name=text.name,
            )
            for text in project.texts
        ],
        music=MusicOut(
            url=await generate_presigned_url(project.music.url),
            duration_seconds=music.duration_seconds,
            bpm=music.bpm,
            custom_bpm=music.custom_bpm,
        )
        if music
        else None,
    )


@router.delete("/{project_id}", summary="Удалить проект", operation_id="delete_project")
async def delete_project(project: ProjectAnnotation, db_session: DBSessionDep):
    """Удалить проект"""
    await db_session.delete(project)
    await db_session.commit()
