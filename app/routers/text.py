from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, status, HTTPException

from app.database import project_texts
from app.routers.dependencies import get_text_by_id
from app.schemas import TextVariant, TextVariantIn, TextVariantWithoutID

router = APIRouter()

TextAnnotation = Annotated[TextVariant, Depends(get_text_by_id)]
TEXT_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "Текста с заданным id не существует"}}


@router.get(
    "/{text_id}",
    summary="Получить вариант текста",
    responses=TEXT_NOT_FOUND
)
async def get_text(text: TextAnnotation) -> TextVariant:
    return text


@router.patch(
    "/{text_id}",
    summary="Изменить вариант текста",
    responses=TEXT_NOT_FOUND
)
async def set_text(old_text: TextAnnotation, new_text: TextVariantWithoutID) -> TextVariant:

    new_values = new_text.model_dump(exclude_unset=True)
    project_texts[old_text.id].update_from_dict(new_values)

    return project_texts[old_text.id]


@router.post(
    "/",
    summary="Создать вариант текста",
    responses=TEXT_NOT_FOUND
)
async def create_text(text: TextVariantIn) -> TextVariant:
    text_id = uuid4()
    text = TextVariant(id=text_id, **text.model_dump(exclude_unset=True))

    return text
