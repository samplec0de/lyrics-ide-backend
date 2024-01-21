"""CRUD текстов"""
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.api.annotations import TextAnnotation, UserAnnotation
from app.api.schemas import TextVariant, TextVariantIn, TextVariantWithoutID
from app.status_codes import TEXT_NOT_FOUND

router = APIRouter()


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
    # new_values = new_text.model_dump(exclude_unset=True)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Текст не найден")


@router.delete("/{text_id}", summary="Удалить вариант текста")
async def delete_project(current_user: UserAnnotation, text: TextAnnotation):
    """Удаление варианта текста"""
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Текст не найден")
