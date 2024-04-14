"""Эндпоинты аутентификации"""
import datetime
import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.api.annotations import TextAnnotation, TextGrantLevelAnnotation
from app.api.dependencies.core import DBSessionDep
from app.auth import Token, check_current_user, create_access_token
from app.config import settings
from app.models import TextModel
from app.models.grant import GrantLevel
from app.status_codes import TEXT_NO_PERMISSIONS

router = APIRouter()


@router.get(
    "/token/{text_id}",
    responses={
        **TEXT_NO_PERMISSIONS,
    },
    dependencies=[Depends(check_current_user)],
    operation_id="get_tiptap_token",
)
async def get_tiptap_access_token(
    grant_level: TextGrantLevelAnnotation,
    text_model: TextAnnotation,
) -> Token:
    """Получение JWT токена для TipTap под конкретный текст.
    {
        "iat": <utcnow()>,
        "iss": "https://lyrics-backend.k8s-1.sslane.ru",
        "nbf": <utcnow()>,
        "aud": <tiptap-app-id>,
        "allowedDocumentNames": [<text_id>],
        "readonlyDocumentNames": [<text_id>] # если grant_level == "READ_ONLY", иначе [] (полный доступ)
    }
    """
    if grant_level is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы не имеете доступа к тексту")

    access_token = create_access_token(
        data={
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "iss": "https://lyrics-backend.k8s-1.sslane.ru",
            "nbf": datetime.datetime.now(datetime.timezone.utc),
            "aud": settings.tiptap_app_id,
            "allowedDocumentNames": [str(text_model.text_id)],
            "readonlyDocumentNames": [str(text_model.text_id)] if grant_level == GrantLevel.READ_ONLY else [],
        },
        secret_key=settings.tiptap_secret_key,
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@router.post(
    "/webhook",
    operation_id="update_text_webhook",
)
async def update_document(json_body: Annotated[dict, Body], db_session: DBSessionDep) -> dict:
    """Webhook, который вызывается TipTap после обновления текста"""
    text_id = uuid.UUID(json_body.get("name"), version=4)
    text_model = await db_session.get(TextModel, text_id)
    if text_model is None:
        return {"message": f"document {text_id} not found"}

    text_model.updated_at = datetime.datetime.now(datetime.timezone.utc)
    print(f"Обновлен текст {text_model.text_id} из TipTap:\n", json_body)

    return {"message": "ok"}
