"""CRUD проектов"""
from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.annotations import ProjectAnnotation
from app.api.dependencies.core import DBSessionDep, MongoDBTextCollectionDep
from app.api.schemas import MusicOut, ProjectBase, ProjectOut, TextVariantCompact
from app.models import ProjectModel, TextModel
from app.s3 import generate_presigned_url
from app.status_codes import PROJECT_NOT_FOUND

router = APIRouter()


@router.post("/", summary="Создать проект", operation_id="create_project")
async def create_project(
    project: ProjectBase, db_session: DBSessionDep, text_collection: MongoDBTextCollectionDep
) -> ProjectOut:
    """Создать проект"""
    new_project = ProjectModel(name=project.name, description=project.description)

    db_session.add(new_project)
    await db_session.commit()
    await db_session.refresh(new_project)

    text_model = TextModel(
        project_id=new_project.project_id,
        name=None,
    )
    db_session.add(text_model)
    await db_session.commit()

    await db_session.refresh(text_model)
    await db_session.refresh(new_project)

    result = await text_collection.insert_one({"_id": str(text_model.text_id), "payload": {}})

    first_text = TextVariantCompact(text_id=result.inserted_id, name=text_model.name)

    return ProjectOut(
        name=new_project.name,
        description=new_project.description,
        project_id=new_project.project_id,
        texts=[first_text],
        music=None,
    )


@router.patch(
    "/{project_id}",
    summary="Изменить проект",
    responses=PROJECT_NOT_FOUND,
    operation_id="update_project",
)
async def update_project(project: ProjectAnnotation, project_data: ProjectBase, db_session: DBSessionDep) -> ProjectOut:
    """Изменить проект"""
    new_values = project_data.model_dump(exclude_unset=True)
    if "name" in new_values:
        project.name = new_values["name"]
    if "description" in new_values:
        project.description = new_values["description"]

    await db_session.commit()
    await db_session.refresh(project)

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
            duration_seconds=project.music.duration_seconds,
            bpm=project.music.bpm,
            custom_bpm=project.music.custom_bpm,
        )
        if project.music
        else None,
    )


@router.get("/", summary="Получить список проектов", operation_id="get_projects")
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


@router.get(
    "/{project_id}",
    summary="Получить содержимое проекта",
    responses=PROJECT_NOT_FOUND,
    operation_id="get_project",
)
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


@router.delete(
    "/{project_id}",
    summary="Удалить проект",
    responses=PROJECT_NOT_FOUND,
    operation_id="delete_project",
)
async def delete_project(project: ProjectAnnotation, db_session: DBSessionDep):
    """Удалить проект"""
    await db_session.delete(project)
    await db_session.commit()
