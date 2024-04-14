"""Аннотации для зависимостей и валидации"""
from typing import Annotated

from fastapi import Depends, Query

from app.api.dependencies.dependencies import (
    get_grant_code_by_id,
    get_project_by_id,
    get_project_by_id_and_grant,
    get_project_by_id_and_owner,
    get_text_access_level,
    get_text_by_id,
    get_text_by_id_and_grant,
    get_text_by_id_and_owner,
    get_tiptap_client,
)
from app.auth import get_current_user
from app.models import ProjectGrantCodeModel, ProjectModel, TextModel, UserModel
from app.models.grant import GrantLevel
from app.tiptap_utils import TipTapClient

ProjectAnnotation = Annotated[ProjectModel, Depends(get_project_by_id)]
OwnProjectAnnotation = Annotated[ProjectModel, Depends(get_project_by_id_and_owner)]
OwnOrGrantProjectAnnotation = Annotated[ProjectModel, Depends(get_project_by_id_and_grant)]
WordAnnotation = Annotated[str, Query(description="слово", min_length=3, max_length=33)]
CurrentUserAnnotation = Annotated[UserModel, Depends(get_current_user)]
TextAnnotation = Annotated[TextModel, Depends(get_text_by_id)]
OwnTextAnnotation = Annotated[TextModel, Depends(get_text_by_id_and_owner)]
OwnOrGrantTextAnnotation = Annotated[TextModel, Depends(get_text_by_id_and_grant)]
TextGrantLevelAnnotation = Annotated[GrantLevel, Depends(get_text_access_level)]
ProjectGrantCodeAnnotation = Annotated[ProjectGrantCodeModel, Depends(get_grant_code_by_id)]
TipTapClientAnnotation = Annotated[TipTapClient, Depends(get_tiptap_client)]
