"""CRUD прав доступа"""
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.annotations import CurrentUserAnnotation, ProjectAnnotation, ProjectGrantCodeAnnotation
from app.api.dependencies.core import DBSessionDep
from app.api.schemas import ProjectGrant, ProjectGrantCode
from app.models.grant import GrantLevel, ProjectGrantCodeModel, ProjectGrantModel
from app.status_codes import GRANT_CODE_MAX_ACTIVATIONS_EXCEEDED, GRANT_CODE_NOT_FOUND, PROJECT_NOT_FOUND

router = APIRouter()


@router.get(
    "/{project_id}",
    summary="Получить код на получение доступа к проекту",
    responses=PROJECT_NOT_FOUND,
    operation_id="generate_project_share_code",
)
async def get_project_share_code(
    project: ProjectAnnotation,
    grant_level: Annotated[GrantLevel, Query(description="уровень доступа")],
    max_activations: Annotated[int, Query(description="максимальное количество активаций", gt=0)],
    db_session: DBSessionDep,
    current_user: CurrentUserAnnotation,
) -> ProjectGrantCode:
    """Получить ссылку на получение доступа к проекту"""
    grant_code = ProjectGrantCodeModel(
        project_id=project.project_id,
        issuer_user_id=current_user.user_id,
        level=grant_level,
        max_activations=max_activations,
    )
    db_session.add(grant_code)
    await db_session.commit()

    await db_session.refresh(grant_code)

    return ProjectGrantCode(
        grant_code_id=grant_code.grant_code_id,
        project_id=grant_code.project_id,
        issuer_user_id=grant_code.issuer_user_id,
        level=grant_code.level,
        max_activations=grant_code.max_activations,
        current_activations=0,
        is_active=True,
        created_at=grant_code.created_at,
        updated_at=grant_code.updated_at,
    )


@router.get(
    "/activate/{grant_code_id}",
    summary="Активировать код доступа к проекту",
    responses={**GRANT_CODE_NOT_FOUND, **GRANT_CODE_MAX_ACTIVATIONS_EXCEEDED},
    operation_id="activate_project_share_code",
)
async def activate_project_share_code(
    grant_code: ProjectGrantCodeAnnotation,
    db_session: DBSessionDep,
    current_user: CurrentUserAnnotation,
) -> ProjectGrant:
    """Активировать код доступа к проекту. Проверяет наличие и активность кода, активирует в случае успеха проерок."""
    if not grant_code.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Код доступа к проекту не найден или деактивирован"
        )

    if grant_code.current_activations >= grant_code.max_activations:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Превышено максимальное количество активаций кода доступа к проекту",
        )

    grant = ProjectGrantModel(
        project_id=grant_code.project_id,
        user_id=current_user.user_id,
        level=grant_code.level,
        grant_code_id=grant_code.grant_code_id,
    )

    db_session.add(grant)
    grant_code.current_activations += 1
    await db_session.commit()
    await db_session.refresh(grant)

    user_email = current_user.email

    return ProjectGrant(
        project_id=grant.project_id,
        user_id=grant.user_id,
        user_email=user_email,
        level=grant.level,
        created_at=grant.created_at,
    )


@router.get(
    "/{project_id}/users",
    summary="Получить список пользователей, имеющих доступ к проекту",
    responses=PROJECT_NOT_FOUND,
    operation_id="get_project_users",
)
async def get_project_users(
    project: ProjectAnnotation,
    db_session: DBSessionDep,
) -> list[ProjectGrant]:
    """Получить список пользователей, имеющих доступ к проекту"""
    # select with additional user field
    result = await db_session.execute(
        select(ProjectGrantModel)
        .options(selectinload(ProjectGrantModel.user))
        .where(ProjectGrantModel.project_id == project.project_id)
        .order_by(ProjectGrantModel.created_at)
    )
    project_grant_models = result.scalars().all()
    return [
        ProjectGrant(
            project_id=project_grant.project_id,
            user_id=project_grant.user_id,
            user_email=project_grant.user.email,
            level=project_grant.level,
            created_at=project_grant.created_at,
        )
        for project_grant in project_grant_models
    ]


# sets is_active=False for project grant
@router.delete(
    "/{project_id}/users/{user_id}",
    summary="Отозвать доступ к проекту",
    responses={
        **PROJECT_NOT_FOUND,
        status.HTTP_404_NOT_FOUND: {"description": "Пользователь не имеет доступа к проекту"},
    },
    operation_id="revoke_project_access",
)
async def revoke_project_access(
    project: ProjectAnnotation,
    user_id: Annotated[str, Path(description="ID пользователя")],
    db_session: DBSessionDep,
) -> None:
    """Отозвать доступ к проекту"""
    result = await db_session.execute(
        select(ProjectGrantModel)
        .where(ProjectGrantModel.project_id == project.project_id)
        .where(ProjectGrantModel.user_id == user_id)
    )
    project_grant = result.scalars().first()
    if project_grant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не имеет доступа к проекту")
    project_grant.is_active = False
    await db_session.commit()
    return None
