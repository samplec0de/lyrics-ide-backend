"""Утилиты для работы с уровнями доступа к проектам"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ProjectGrantModel
from app.models.grant import GrantLevel


async def get_grant_level_by_user_and_project(
    user_id: uuid.UUID, project_id: uuid.UUID, db_session: AsyncSession
) -> GrantLevel | None:
    """Получить уровень доступа пользователя к проекту"""
    project_grant_query = await db_session.execute(
        select(ProjectGrantModel.level)
        .where(ProjectGrantModel.user_id == user_id)
        .where(ProjectGrantModel.project_id == project_id)
    )
    project_grant = project_grant_query.scalars().first()
    return project_grant
