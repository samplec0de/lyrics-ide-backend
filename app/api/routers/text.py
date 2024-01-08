"""CRUD текстов"""
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends

from app.api.annotations import UserAnnotation
from app.api.dependencies.dependencies import get_text_by_id
from app.api.schemas import TextVariant, TextVariantIn, TextVariantWithoutID
from app.database_dumb import project_texts
from app.status_codes import TEXT_NOT_FOUND

router = APIRouter()

TextAnnotation = Annotated[TextVariant, Depends(get_text_by_id)]


@router.post("/", summary="Создать вариант текста", responses=TEXT_NOT_FOUND)
async def create_text(current_user: UserAnnotation, text_in: TextVariantIn) -> TextVariant:
    """Создание варианта текста"""
    text_id = uuid4()
    text = TextVariant(id=text_id, **text_in.model_dump(exclude_unset=True))

    return text


@router.get("/{text_id}", summary="Получить вариант текста", responses=TEXT_NOT_FOUND)
async def get_text(current_user: UserAnnotation, text: TextAnnotation) -> TextVariant:
    """Получение варианта текста"""
    return text


@router.patch("/{text_id}", summary="Изменить вариант текста", responses=TEXT_NOT_FOUND)
async def set_text(
    current_user: UserAnnotation, old_text: TextAnnotation, new_text: TextVariantWithoutID
) -> TextVariant:
    """Изменение варианта текста"""
    new_values = new_text.model_dump(exclude_unset=True)
    project_texts[old_text.id] = old_text.model_copy(update=new_values)

    return project_texts[old_text.id]


@router.delete("/{text_id}", summary="Удалить вариант текста")
async def delete_project(current_user: UserAnnotation, text: TextAnnotation):
    """Удаление варианта текста"""
    project_texts.pop(text.id)
