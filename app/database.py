from pydantic import UUID4

from app.schemas import ProjectOut, TextVariant

projects: dict[UUID4, ProjectOut] = {}
project_texts: dict[UUID4, TextVariant] = {}
