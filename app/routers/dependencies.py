from typing import Annotated

from fastapi import status, HTTPException, Path
from pydantic import UUID4

from app.database import projects, project_texts
from app.schemas import ProjectOut, TextVariant


async def get_project_by_id(
        project_id: Annotated[UUID4, Path(description="Идентификатор проекта")]
) -> ProjectOut:
    if project_id not in projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден")

    return projects[project_id]


async def get_text_by_id(
        text_id: Annotated[UUID4, Path(description="Идентификатор варианта текста")]
) -> TextVariant:
    if text_id not in projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Текст не найден")

    return project_texts[text_id]
