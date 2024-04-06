"""Эндпоинты аутентификации"""
from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from app.api.annotations import TextAnnotation, TextGrantLevelAnnotation
from app.auth import Token, create_access_token
from app.config import settings
from app.models.grant import GrantLevel
from app.status_codes import TEXT_NO_PERMISSIONS

router = APIRouter()


@router.get(
    "/token/{text_id}",
    responses={
        **TEXT_NO_PERMISSIONS,
    },
    operation_id="get_tiptap_token",
)
async def get_tiptap_access_token_v2(
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
            "iat": datetime.utcnow(),
            "iss": "https://lyrics-backend.k8s-1.sslane.ru",
            "nbf": datetime.utcnow(),
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
