"""Зависимости для валидации данных в пути запроса"""
from typing import Annotated, cast

from fastapi import Depends, HTTPException, Path, status
from pydantic import UUID4
from sqlalchemy import ColumnElement, select
from sqlalchemy.orm import selectinload

from app.api.dependencies.core import DBSessionDep
from app.auth import get_current_user
from app.models import ProjectGrantCodeModel, ProjectGrantModel, ProjectModel, TextModel, UserModel
from app.models.grant import GrantLevel


async def get_project_by_id(
    project_id: Annotated[UUID4, Path(description="Идентификатор проекта")], db_session: DBSessionDep
) -> ProjectModel:
    """Получить проект по его идентификатору"""
    result = await db_session.execute(
        select(ProjectModel)
        .options(selectinload(ProjectModel.music), selectinload(ProjectModel.texts))
        .where(ProjectModel.project_id == project_id)
    )
    project = result.scalars().first()

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден")

    return project


async def get_project_by_id_and_owner(
    project_id: Annotated[UUID4, Path(description="Идентификатор проекта")],
    current_user: Annotated[UserModel, Depends(get_current_user)],
    db_session: DBSessionDep,
) -> ProjectModel:
    """Получить проект по его идентификатору и проверить, что пользователь является владельцем"""
    project = await get_project_by_id(project_id, db_session)
    if project.owner_user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы не владелец проекта")

    return project


async def get_project_by_id_and_grant(
    project_id: Annotated[UUID4, Path(description="Идентификатор проекта")],
    current_user: Annotated[UserModel, Depends(get_current_user)],
    db_session: DBSessionDep,
) -> ProjectModel:
    """Получить проект по его идентификатору и проверить, что пользователь имеет доступ к проекту"""
    result = await db_session.execute(
        select(ProjectModel)
        .options(selectinload(ProjectModel.music), selectinload(ProjectModel.texts))
        .where(ProjectModel.project_id == project_id)
    )
    project = result.scalars().first()

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден")

    if project.owner_user_id != current_user.user_id:
        result = await db_session.execute(
            select(ProjectGrantModel)
            .where(ProjectGrantModel.project_id == project_id)
            .where(ProjectGrantModel.user_id == current_user.user_id)
            .where(ProjectGrantModel.is_active.is_(True))
        )
        grant_code = result.scalars().first()
        if grant_code is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы не имеете доступа к проекту")

    return project


async def get_text_by_id(
    text_id: Annotated[UUID4, Path(description="Идентификатор варианта текста")], db_session: DBSessionDep
) -> TextModel:
    """Получить вариант текста по его идентификатору"""
    result = await db_session.execute(
        select(TextModel)
        .options(selectinload(TextModel.project))
        .where(cast(ColumnElement[bool], TextModel.text_id == text_id))
    )
    text = result.scalars().first()
    if text is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Текст не найден")

    return text


async def get_text_by_id_and_owner(
    text_id: Annotated[UUID4, Path(description="Идентификатор текста")],
    current_user: Annotated[UserModel, Depends(get_current_user)],
    db_session: DBSessionDep,
) -> TextModel:
    """Получить текст по его идентификатору и проверить, что пользователь является владельцем"""
    text = await get_text_by_id(text_id, db_session)
    project = text.project
    if project.owner_user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы не владелец проекта")

    return text


async def get_text_access_level(
    text: Annotated[TextModel, Depends(get_text_by_id)],
    current_user: Annotated[UserModel, Depends(get_current_user)],
    db_session: DBSessionDep,
) -> GrantLevel | None:
    """Получить значение уровеня доступа к тексту

    :return: уровень доступа к тексту, GrantLevel.READ_ONLY или GrantLevel.READ_WRITE
    если пользователь владелец, то возвращается GrantLevel.READ_WRITE
    """
    if text.project.owner_user_id == current_user.user_id:
        return GrantLevel.READ_WRITE

    result = await db_session.execute(
        select(ProjectGrantModel)
        .where(ProjectGrantModel.project_id == text.project_id)
        .where(ProjectGrantModel.user_id == current_user.user_id)
        .where(ProjectGrantModel.is_active.is_(True))
    )
    grant = result.scalars().first()
    if grant is None:
        return None

    return grant.level


async def get_text_by_id_and_grant(
    text_id: Annotated[UUID4, Path(description="Идентификатор текста")],
    grant_level: Annotated[GrantLevel, Depends(get_text_access_level)],
    current_user: Annotated[UserModel, Depends(get_current_user)],
    db_session: DBSessionDep,
) -> TextModel:
    """Получить текст по его идентификатору и проверить, что пользователь имеет доступ к проекту"""
    text = await get_text_by_id(text_id, db_session)
    if grant_level is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы не имеете доступа к проекту")

    return text


async def get_grant_code_by_id(
    grant_code_id: Annotated[UUID4, Path(description="Идентификатор кода доступа")], db_session: DBSessionDep
) -> ProjectGrantCodeModel:
    """Получить код доступа по его идентификатору"""
    result = await db_session.execute(
        select(ProjectGrantCodeModel)
        .options(selectinload(ProjectGrantCodeModel.project))
        .where(ProjectGrantCodeModel.grant_code_id == grant_code_id)
    )
    grant_code = result.scalars().first()
    if grant_code is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Код доступа к проекту не найден или деактивирован"
        )

    return grant_code
