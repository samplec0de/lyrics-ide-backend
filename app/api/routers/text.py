"""CRUD текстов"""
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select

from app.api.annotations import TextAnnotation
from app.api.dependencies.core import DBSessionDep, MongoDBTextCollectionDep
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
async def create_text(
    text_in: TextVariantIn, db_session: DBSessionDep, text_collection: MongoDBTextCollectionDep
) -> TextVariant:
    """Создание варианта текста"""
    text_model = TextModel(
        project_id=text_in.project_id,
        name=text_in.name,
    )
    db_session.add(text_model)
    await db_session.commit()

    await db_session.refresh(text_model)

    result = await text_collection.insert_one({"_id": str(text_model.text_id), "payload": {}})

    text_schema = TextVariant(text_id=result.inserted_id, name=text_model.name, payload={})

    return text_schema


@router.get(
    "/{text_id}",
    summary="Получить вариант текста",
    responses=TEXT_NOT_FOUND,
    operation_id="get_text",
)
async def get_text(text: TextAnnotation, text_collection: MongoDBTextCollectionDep) -> TextVariant:
    """Получение варианта текста"""
    text_data = await text_collection.find_one({"_id": str(text.text_id)}) or {}
    return TextVariant(
        text_id=text.text_id,
        name=text.name,
        payload=text_data.get("payload", {}),
    )


@router.patch(
    "/{text_id}",
    summary="Изменить вариант текста",
    responses=TEXT_NOT_FOUND,
    operation_id="update_text",
)
async def update_text(
    old_text: TextAnnotation,
    new_text: TextVariantWithoutID,
    db_session: DBSessionDep,
    text_collection: MongoDBTextCollectionDep,
) -> TextVariant:
    """Изменение варианта текста"""
    new_values = new_text.model_dump(exclude_unset=True)
    actual_payload = None
    if "payload" in new_values:
        await text_collection.update_one({"_id": str(old_text.text_id)}, {"$set": {"payload": new_values["payload"]}})
        actual_payload = new_values["payload"]

    if "name" in new_values:
        old_text.name = new_text.name

    if actual_payload is None:
        actual_payload = (await text_collection.find_one({"_id": str(old_text.text_id)}) or {}).get("payload", {})

    new_text_schema = TextVariant(
        text_id=old_text.text_id,
        name=old_text.name,
        payload=actual_payload,
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
async def delete_text(
    text: TextAnnotation, db_session: DBSessionDep, text_collection: MongoDBTextCollectionDep
) -> None:
    """Удаление варианта текста"""
    # pylint: disable=not-callable
    count_query = await db_session.execute(select(func.count()).where(TextModel.project_id == text.project_id))
    # pylint: enable=not-callable
    count = count_query.scalar_one()
    if count == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Нельзя удалить единственный текст из проекта"
        )

    await text_collection.delete_one({"_id": str(text.text_id)})
    await db_session.delete(text)
    await db_session.commit()
