"""Зависимости для валидации данных в пути запроса"""
from typing import Annotated

from fastapi import HTTPException, Path, status
from pydantic import UUID4

from app.api.dependencies.core import DBSessionDep
from app.api.schemas import TextVariant
from app.database_dumb import project_texts
from app.models import ProjectModel


async def get_project_by_id(
    project_id: Annotated[UUID4, Path(description="Идентификатор проекта")], db_session: DBSessionDep
) -> ProjectModel:
    """Получить проект по его идентификатору"""
    project = await db_session.get(ProjectModel, project_id)

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден")

    return project


async def get_text_by_id(text_id: Annotated[UUID4, Path(description="Идентификатор варианта текста")]) -> TextVariant:
    """Получить вариант текста по его идентификатору"""
    if text_id not in project_texts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Текст не найден")

    return project_texts[text_id]
