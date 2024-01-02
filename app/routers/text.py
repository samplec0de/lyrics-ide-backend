from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.routers.dependencies import get_text_by_id
from app.schemas import TextVariant

router = APIRouter()

TextAnnotation = Annotated[TextVariant, Depends(get_text_by_id)]
TEXT_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "Текста с заданным id не существует"}}


@router.get(
    "/{text_id}",
    summary="Получить текст варианта",
    responses=TEXT_NOT_FOUND
)
async def get_text(text: TextAnnotation) -> TextVariant:
    return text
