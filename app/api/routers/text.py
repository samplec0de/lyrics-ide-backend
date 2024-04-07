"""CRUD текстов"""
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select

from app.api.annotations import OwnOrGrantTextAnnotation, OwnTextAnnotation
from app.api.dependencies.core import DBSessionDep
from app.api.schemas import TextVariant, TextVariantIn, TextVariantWithoutID
from app.models import TextModel
from app.status_codes import CANNOT_REMOVE_SINGLE_TEXT, PROJECT_NOT_FOUND, TEXT_NOT_FOUND

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
    )
    db_session.add(text_model)
    await db_session.commit()

    await db_session.refresh(text_model)

    text_schema = TextVariant(
        text_id=text_model.text_id,
        name=text_model.name,
        created_at=text_model.created_at,
        updated_at=text_model.updated_at,
        payload={},
    )

    return text_schema


@router.get(
    "/{text_id}",
    summary="Получить вариант текста",
    responses=TEXT_NOT_FOUND,
    operation_id="get_text",
)
async def get_text(text: OwnOrGrantTextAnnotation) -> TextVariant:
    """Получение варианта текста"""
    return TextVariant(
        text_id=text.text_id,
        name=text.name,
        created_at=text.created_at,
        updated_at=text.updated_at,
        payload={},
    )


@router.patch(
    "/{text_id}",
    summary="Изменить вариант текста",
    responses=TEXT_NOT_FOUND,
    operation_id="update_text",
)
async def update_text(
    old_text: OwnTextAnnotation,
    new_text: TextVariantWithoutID,
    db_session: DBSessionDep,
) -> TextVariant:
    """Изменение варианта текста"""
    new_values = new_text.model_dump(exclude_unset=True)

    if "name" in new_values:
        old_text.name = new_text.name

    new_text_schema = TextVariant(
        text_id=old_text.text_id,
        name=old_text.name,
        created_at=old_text.created_at,
        updated_at=old_text.updated_at,
        payload={},
    )

    db_session.add(old_text)
    await db_session.commit()

    return new_text_schema


@router.delete(
    "/{text_id}",
    summary="Удалить вариант текста",
    responses={**TEXT_NOT_FOUND, **CANNOT_REMOVE_SINGLE_TEXT},
    operation_id="delete_text",
)
async def delete_text(text: OwnTextAnnotation, db_session: DBSessionDep) -> None:
    """Удаление варианта текста"""
    # pylint: disable=not-callable
    count_query = await db_session.execute(select(func.count()).where(TextModel.project_id == text.project_id))
    # pylint: enable=not-callable
    count = count_query.scalar_one()
    if count == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Нельзя удалить единственный текст из проекта"
        )

    await db_session.delete(text)
    await db_session.commit()
