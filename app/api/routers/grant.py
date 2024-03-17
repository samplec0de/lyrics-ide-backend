"""CRUD прав доступа"""
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.api.annotations import ProjectAnnotation, ProjectGrantCodeAnnotation, UserAnnotation
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
    current_user: UserAnnotation,
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
    current_user: UserAnnotation,
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
    )

    db_session.add(grant)
    grant_code.current_activations += 1
    await db_session.commit()
    await db_session.refresh(grant)

    return ProjectGrant(
        project_id=grant.project_id,
        user_id=grant.user_id,
        level=grant.level,
        created_at=grant.created_at,
    )
