from pydantic import UUID4

from app.schemas import ProjectOut

projects: dict[UUID4, ProjectOut] = {}
