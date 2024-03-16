"""Аннотации для зависимостей и валидации"""
from typing import Annotated

from fastapi import Depends, Query

from app.api.dependencies.dependencies import get_project_by_id, get_text_by_id
from app.auth import get_current_user
from app.models import ProjectModel, TextModel, UserModel

ProjectAnnotation = Annotated[ProjectModel, Depends(get_project_by_id)]
WordAnnotation = Annotated[str, Query(description="слово", min_length=3, max_length=33)]
UserAnnotation = Annotated[UserModel, Depends(get_current_user)]
TextAnnotation = Annotated[TextModel, Depends(get_text_by_id)]
