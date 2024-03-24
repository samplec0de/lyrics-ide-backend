"""Аннотации для зависимостей и валидации"""
from typing import Annotated

from fastapi import Depends, Query

from app.api.dependencies.dependencies import get_grant_code_by_id, get_project_by_id, get_text_by_id
from app.auth import get_current_user
from app.models import ProjectGrantCodeModel, ProjectModel, TextModel, UserModel

ProjectAnnotation = Annotated[ProjectModel, Depends(get_project_by_id)]
WordAnnotation = Annotated[str, Query(description="слово", min_length=3, max_length=33)]
CurrentUserAnnotation = Annotated[UserModel, Depends(get_current_user)]
TextAnnotation = Annotated[TextModel, Depends(get_text_by_id)]
ProjectGrantCodeAnnotation = Annotated[ProjectGrantCodeModel, Depends(get_grant_code_by_id)]
