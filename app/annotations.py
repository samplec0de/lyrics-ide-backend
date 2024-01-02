from typing import Annotated

from fastapi import Depends, Query

from app.auth import User, get_current_user
from app.routers.dependencies import get_project_by_id
from app.schemas import ProjectOut

ProjectAnnotation = Annotated[ProjectOut, Depends(get_project_by_id)]
WordAnnotation = Annotated[str, Query(description="слово", min_length=3, max_length=33)]
UserAnnotation = Annotated[User, Depends(get_current_user)]
