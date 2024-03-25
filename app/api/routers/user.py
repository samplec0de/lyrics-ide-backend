"""Вспомогательные эндпоинты для работы с пользователями"""
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status
from pydantic import UUID4

from app.api.annotations import CurrentUserAnnotation
from app.api.schemas import UserOut
from app.status_codes import NO_ACCESS_TO_USER_INFO, USER_NOT_FOUND

router = APIRouter()


@router.get(
    "/{user_id}",
    summary="Получить информацию о пользователе",
    responses={
        **USER_NOT_FOUND,
        **NO_ACCESS_TO_USER_INFO,
    },
    operation_id="get_user",
)
async def get_user(
    user_id: Annotated[UUID4, Path(description="ID пользователя")], current_user: CurrentUserAnnotation
) -> UserOut:
    """Получить информацию о пользователе. Можно получить информацию только про себя."""
    if user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="У вас нет доступа к информации о пользователе"
        )

    return UserOut(
        user_id=current_user.user_id,
        email=current_user.email,
    )
