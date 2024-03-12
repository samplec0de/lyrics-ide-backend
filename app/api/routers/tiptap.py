"""Эндпоинты аутентификации"""
from datetime import datetime

from fastapi import APIRouter

from app.auth import Token, create_access_token
from app.config import settings

router = APIRouter()


@router.get("/token", response_model=Token, operation_id="get_tiptap_access_token")
async def get_tiptap_access_token():
    """Получение JWT токена для TipTap.
    {"iat": <utcnow()>, "iss": "https://lyrics-backend.k8s-1.sslane.ru", "nbf": <utcnow()>, "aud": <tiptap-app-id>}
    """
    access_token = create_access_token(
        data={
            "iat": datetime.utcnow(),
            "iss": "https://lyrics-backend.k8s-1.sslane.ru",
            "nbf": datetime.utcnow(),
            "aud": settings.tiptap_app_id,
        },
        secret_key=settings.tiptap_secret_key,
    )
    return {"access_token": access_token, "token_type": "bearer"}
