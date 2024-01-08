"""Аннотации для зависимостей и валидации"""
from typing import Annotated

from fastapi import Depends, Query

from app.api.dependencies.dependencies import get_project_by_id
from app.api.schemas import ProjectOut
from app.auth import User, get_current_user

ProjectAnnotation = Annotated[ProjectOut, Depends(get_project_by_id)]
WordAnnotation = Annotated[str, Query(description="слово", min_length=3, max_length=33)]
UserAnnotation = Annotated[User, Depends(get_current_user)]
