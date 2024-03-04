"""CRUD текстов"""
from fastapi import APIRouter

from app.api.annotations import TextAnnotation
from app.api.dependencies.core import DBSessionDep
from app.api.schemas import TextVariant, TextVariantIn, TextVariantWithoutID
from app.models import TextModel
from app.status_codes import PROJECT_NOT_FOUND, TEXT_NOT_FOUND

router = APIRouter()


@router.post(
    "/",
    summary="Создать вариант текста",
    responses=PROJECT_NOT_FOUND,
    operation_id="create_text",
)
async def create_text(text_in: TextVariantIn, db_session: DBSessionDep) -> TextVariant:
    """Создание варианта текста"""
    text_model = TextModel(
        project_id=text_in.project_id,
        name=text_in.name,
        url="https://lyrics-ide.storage.yandexcloud.net/text_stub.json",
    )
    db_session.add(text_model)
    await db_session.commit()

    await db_session.refresh(text_model)

    text_schema = TextVariant(text_id=text_model.text_id, name=text_model.name, text="")

    return text_schema


@router.get(
    "/{text_id}",
    summary="Получить вариант текста",
    responses=TEXT_NOT_FOUND,
    operation_id="get_text",
)
async def get_text(text: TextAnnotation) -> TextVariant:
    """Получение варианта текста"""
    return TextVariant(
        text_id=text.text_id,
        name=text.name,
        text="Тут должен быть текст, но пока затычка",
    )


@router.patch(
    "/{text_id}",
    summary="Изменить вариант текста",
    responses=TEXT_NOT_FOUND,
    operation_id="update_text",
)
async def update_text(
    old_text: TextAnnotation, new_text: TextVariantWithoutID, db_session: DBSessionDep
) -> TextVariant:
    """Изменение варианта текста"""
    new_values = new_text.model_dump(exclude_unset=True)
    if "text" in new_values:
        old_text.url = "https://lyrics-ide.storage.yandexcloud.net/text_stub_new.json"

    if "name" in new_values:
        old_text.name = new_text.name

    new_text_schema = TextVariant(
        text_id=old_text.text_id,
        name=old_text.name,
        text="Тут должен быть текст, но пока затычка",
    )

    db_session.add(old_text)
    await db_session.commit()

    return new_text_schema


@router.delete("/{text_id}", summary="Удалить вариант текста", operation_id="delete_text")
async def delete_text(text: TextAnnotation, db_session: DBSessionDep) -> None:
    """Удаление варианта текста"""
    await db_session.delete(text)
    await db_session.commit()
