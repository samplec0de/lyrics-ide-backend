"""CRUD прав доступа"""
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.api.annotations import CurrentUserAnnotation, OwnProjectAnnotation, ProjectGrantCodeAnnotation
from app.api.dependencies.core import DBSessionDep
from app.api.schemas import ProjectGrant, ProjectGrantCode
from app.models.grant import GrantLevel, ProjectGrantCodeModel, ProjectGrantModel
from app.status_codes import GRANT_CODE_NOT_FOUND, PROJECT_NOT_FOUND, PROJECT_NOT_OWNER

router = APIRouter()


@router.get(
    "/project/{project_id}",
    summary="Получить код на получение доступа к проекту",
    responses={
        **PROJECT_NOT_FOUND,
        **PROJECT_NOT_OWNER,
    },
    operation_id="generate_project_share_code",
)
async def get_project_share_code(
    project: OwnProjectAnnotation,
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
    "/codes/activate/{grant_code_id}",
    summary="Активировать код доступа к проекту",
    responses={
        **GRANT_CODE_NOT_FOUND,
        status.HTTP_403_FORBIDDEN: {
            "description": "Повторная активация кода одним пользователем / "
            "превышено максимальное количество активаций кода доступа к проекту / "
            "владелец проекта не может активировать код доступа к проекту (в ошибке будет указана точная причина)"
        },
    },
    operation_id="activate_project_share_code",
)
async def activate_project_share_code(
    grant_code: ProjectGrantCodeAnnotation,
    db_session: DBSessionDep,
    current_user: CurrentUserAnnotation,
) -> ProjectGrant:
    """Активировать код доступа к проекту.
    Проверяет наличие и активность кода, активирует в случае успеха проверок.
    В случае, когда пользователь активирует новый код доступа по проекту, предыдущий доступ перезаписывается.
    """
    if not grant_code.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Код доступа к проекту не найден или деактивирован"
        )

    if grant_code.current_activations >= grant_code.max_activations:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Превышено максимальное количество активаций кода доступа к проекту",
        )

    if grant_code.project.owner_user_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Владелец проекта не может активировать код доступа к проекту",
        )

    old_grants_query = await db_session.execute(
        select(ProjectGrantModel)
        .where(ProjectGrantModel.project_id == grant_code.project_id)
        .where(ProjectGrantModel.user_id == current_user.user_id)
    )
    old_grants = old_grants_query.scalars().all()
    for old_grant in old_grants:
        await db_session.delete(old_grant)

    await db_session.commit()

    grant = ProjectGrantModel(
        project_id=grant_code.project_id,
        user_id=current_user.user_id,
        level=grant_code.level,
        grant_code_id=grant_code.grant_code_id,
    )

    db_session.add(grant)
    grant_code.current_activations += 1
    try:
        await db_session.commit()
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Повторная активация доступа возможна только по новой ссылке (коду)",
        ) from exc

    await db_session.refresh(grant)

    user_email = current_user.email

    return ProjectGrant(
        grant_code_id=grant_code.grant_code_id,
        project_id=grant.project_id,
        user_id=grant.user_id,
        user_email=user_email,
        level=grant.level,
        is_active=grant.is_active,
        created_at=grant.created_at,
    )


@router.get(
    "/project/{project_id}/users",
    summary="Получить список пользователей, имеющих доступ к проекту",
    responses={
        **PROJECT_NOT_FOUND,
        **PROJECT_NOT_OWNER,
    },
    operation_id="get_project_users",
)
async def get_project_users(
    project: OwnProjectAnnotation,
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
            grant_code_id=project_grant.grant_code_id,
            project_id=project_grant.project_id,
            user_id=project_grant.user_id,
            user_email=project_grant.user.email,
            level=project_grant.level,
            is_active=project_grant.is_active,
            created_at=project_grant.created_at,
        )
        for project_grant in project_grant_models
    ]


@router.delete(
    "/{project_id}/users/{user_id}",
    summary="Отозвать доступ к проекту",
    responses={
        **PROJECT_NOT_FOUND,
        **PROJECT_NOT_OWNER,
        status.HTTP_404_NOT_FOUND: {"description": "Пользователь не имеет доступа к проекту"},
    },
    operation_id="revoke_project_access",
)
async def revoke_project_access(
    project: OwnProjectAnnotation,
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


@router.get(
    "/projects/{project_id}/codes",
    summary="Получить список кодов доступа к проекту",
    responses={
        **PROJECT_NOT_FOUND,
        **PROJECT_NOT_OWNER,
    },
    operation_id="get_project_codes",
)
async def get_project_codes(
    project: OwnProjectAnnotation,
    db_session: DBSessionDep,
) -> list[ProjectGrantCode]:
    """Получить список кодов доступа к проекту"""
    result = await db_session.execute(
        select(ProjectGrantCodeModel).where(ProjectGrantCodeModel.project_id == project.project_id)
    )
    project_grant_codes = result.scalars().all()
    return [
        ProjectGrantCode(
            grant_code_id=project_grant_code.grant_code_id,
            project_id=project_grant_code.project_id,
            issuer_user_id=project_grant_code.issuer_user_id,
            level=project_grant_code.level,
            max_activations=project_grant_code.max_activations,
            current_activations=project_grant_code.current_activations,
            is_active=project_grant_code.is_active,
            created_at=project_grant_code.created_at,
            updated_at=project_grant_code.updated_at,
        )
        for project_grant_code in project_grant_codes
    ]


@router.delete(
    "/codes/{grant_code_id}",
    summary="Деактивировать код доступа к проекту",
    responses={
        **PROJECT_NOT_OWNER,
        **GRANT_CODE_NOT_FOUND,
    },
    operation_id="deactivate_project_grant_code",
)
async def deactivate_project_grant_code(
    grant_code: ProjectGrantCodeAnnotation,
    db_session: DBSessionDep,
) -> None:
    """Деактивировать код доступа к проекту
    (пользователи не блокируются, только запрещается подключение новых по этой ссылке)"""
    project = grant_code.project
    if project.owner_user_id != grant_code.issuer_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы не владелец проекта")
    grant_code.is_active = False
    await db_session.commit()
    return None


@router.patch(
    "/{project_id}/users/{user_id}",
    summary="Изменить уровень доступа",
    responses={
        **PROJECT_NOT_FOUND,
        **PROJECT_NOT_OWNER,
        status.HTTP_404_NOT_FOUND: {"description": "Пользователь не имеет доступа к проекту"},
    },
    operation_id="update_project_access",
)
async def update_project_access(
    project: OwnProjectAnnotation,
    user_id: Annotated[str, Path(description="ID пользователя")],
    new_level: Annotated[GrantLevel, Query(description="новый уровень доступа")],
    db_session: DBSessionDep,
) -> ProjectGrant:
    """Изменить уровень доступа к проекту"""
    result = await db_session.execute(
        select(ProjectGrantModel)
        .options(selectinload(ProjectGrantModel.user))
        .where(ProjectGrantModel.project_id == project.project_id)
        .where(ProjectGrantModel.user_id == user_id)
    )
    project_grant = result.scalars().first()
    if project_grant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не имеет доступа к проекту")
    project_grant.level = new_level
    project_grant.is_active = True
    await db_session.commit()
    return ProjectGrant(
        grant_code_id=project_grant.grant_code_id,
        project_id=project_grant.project_id,
        user_id=project_grant.user_id,
        user_email=project_grant.user.email,
        level=project_grant.level,
        is_active=project_grant.is_active,
        created_at=project_grant.created_at,
    )
