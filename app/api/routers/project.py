"""CRUD проектов"""
import itertools

from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.annotations import CurrentUserAnnotation, OwnOrGrantProjectAnnotation, OwnProjectAnnotation
from app.api.dependencies.core import DBSessionDep
from app.api.schemas import MusicOut, ProjectBase, ProjectOut, TextVariantCompact
from app.grant_utils import get_grant_level_by_user_and_project
from app.models import ProjectModel, TextModel
from app.models.grant import ProjectGrantCodeModel, ProjectGrantModel
from app.s3_helpers import delete, generate_presigned_url
from app.status_codes import PROJECT_NO_PERMISSIONS, PROJECT_NOT_FOUND, PROJECT_NOT_OWNER

router = APIRouter()


@router.post("/", summary="Создать проект", operation_id="create_project")
async def create_project(
    project: ProjectBase,
    current_user: CurrentUserAnnotation,
    db_session: DBSessionDep,
) -> ProjectOut:
    """Создать проект"""
    new_project = ProjectModel(owner_user_id=current_user.user_id, name=project.name, description=project.description)

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

    first_text = TextVariantCompact(
        text_id=text_model.text_id,
        name=text_model.name,
        created_at=text_model.created_at,
        updated_at=text_model.updated_at,
    )

    project_out = ProjectOut(
        name=new_project.name,
        description=new_project.description,
        owner_user_id=new_project.owner_user_id,
        is_owner=True,
        grant_level=None,
        created_at=new_project.created_at,
        updated_at=new_project.updated_at,
        project_id=new_project.project_id,
        texts=[first_text],
        music=None,
    )

    await db_session.refresh(current_user)

    return project_out


@router.patch(
    "/{project_id}",
    summary="Изменить проект. Уровень доступа: владелец проекта",
    responses={
        **PROJECT_NOT_FOUND,
        **PROJECT_NOT_OWNER,
    },
    operation_id="update_project",
)
async def update_project(
    project: OwnProjectAnnotation, project_data: ProjectBase, db_session: DBSessionDep
) -> ProjectOut:
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
        owner_user_id=project.owner_user_id,
        is_owner=True,
        grant_level=None,
        created_at=project.created_at,
        updated_at=project.updated_at,
        project_id=project.project_id,
        texts=[
            TextVariantCompact(
                text_id=text.text_id,
                name=text.name,
                created_at=text.created_at,
                updated_at=text.updated_at,
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
async def get_projects(db_session: DBSessionDep, current_user: CurrentUserAnnotation) -> list[ProjectOut]:
    """Получить список проектов, на которые у пользователя есть доступ"""
    query_grants = await db_session.execute(
        select(ProjectModel)
        .options(selectinload(ProjectModel.music), selectinload(ProjectModel.texts))
        .join(ProjectGrantModel)
        .where(ProjectGrantModel.user_id == current_user.user_id)
        .where(ProjectGrantModel.is_active.is_(True))
    )
    projects_grants = query_grants.scalars().all()

    query_ownership = await db_session.execute(
        select(ProjectModel)
        .options(selectinload(ProjectModel.music), selectinload(ProjectModel.texts))
        .where(ProjectModel.owner_user_id == current_user.user_id)
    )
    projects_ownership = query_ownership.scalars().all()

    return [
        ProjectOut(
            name=project.name,
            description=project.description,
            owner_user_id=project.owner_user_id,
            is_owner=project.owner_user_id == current_user.user_id,
            grant_level=await get_grant_level_by_user_and_project(
                user_id=current_user.user_id, project_id=project.project_id, db_session=db_session
            ),
            created_at=project.created_at,
            updated_at=project.updated_at,
            project_id=project.project_id,
            texts=[
                TextVariantCompact(
                    text_id=text.text_id,
                    name=text.name,
                    created_at=text.created_at,
                    updated_at=text.updated_at,
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
        for project in itertools.chain(projects_grants, projects_ownership)
    ]


@router.get(
    "/{project_id}",
    summary="Получить содержимое проекта",
    responses={
        **PROJECT_NOT_FOUND,
        **PROJECT_NO_PERMISSIONS,
    },
    operation_id="get_project",
)
async def get_project(
    project: OwnOrGrantProjectAnnotation, current_user: CurrentUserAnnotation, db_session: DBSessionDep
) -> ProjectOut:
    """Получить содержимое проекта"""
    music = project.music

    user_grant_level = await get_grant_level_by_user_and_project(
        user_id=current_user.user_id, project_id=project.project_id, db_session=db_session
    )

    return ProjectOut(
        name=project.name,
        description=project.description,
        owner_user_id=project.owner_user_id,
        is_owner=project.owner_user_id == current_user.user_id,
        grant_level=user_grant_level,
        created_at=project.created_at,
        updated_at=project.updated_at,
        project_id=project.project_id,
        texts=[
            TextVariantCompact(
                text_id=text.text_id,
                name=text.name,
                created_at=text.created_at,
                updated_at=text.updated_at,
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
async def delete_project(project: OwnProjectAnnotation, db_session: DBSessionDep):
    """Удалить проект. Приводит к удалению всех текстов проекта, музыки, кодов доступа и прав."""
    texts_query = await db_session.execute(select(TextModel).where(TextModel.project_id == project.project_id))
    texts = texts_query.scalars().all()
    for text in texts:
        await db_session.delete(text)

    if project.music:
        await delete(project.music.url)
        await db_session.delete(project.music)
        await db_session.commit()
        await db_session.refresh(project)

    project_grants_query = await db_session.execute(
        select(ProjectGrantModel).where(ProjectGrantModel.project_id == project.project_id)
    )
    project_grants = project_grants_query.scalars().all()
    for grant in project_grants:
        await db_session.delete(grant)

    project_grant_codes_query = await db_session.execute(
        select(ProjectGrantCodeModel).where(ProjectGrantCodeModel.project_id == project.project_id)
    )
    project_grant_codes = project_grant_codes_query.scalars().all()
    for grant_code in project_grant_codes:
        await db_session.delete(grant_code)

    await db_session.delete(project)
    await db_session.commit()
