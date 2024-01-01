from typing import Annotated

from fastapi import status, HTTPException, Path
from pydantic import UUID4

from app.database import projects
from app.schemas import ProjectOut


async def get_project_by_id(
        project_id: Annotated[UUID4, Path(title="Идентификатор проекта", description="Идентификатор проекта")]
) -> ProjectOut:
    if project_id not in projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден")

    return projects[project_id]
