"""Миксин для работы с редактором текста TipTap"""
import uuid

from httpx import AsyncClient
from jose import jwt

from tests.integration_tests.test_client.components.exceptions import TextNotFoundError, PermissionDeniedError


class Token:
    """Токен для редактора текста"""

    def __init__(self, access_token: str, token_type: str):
        self.access_token = access_token
        self.token_type = token_type

    async def payload(self) -> dict:
        """Получить payload токена"""
        jwt_payload = jwt.decode(self.access_token, "", options={"verify_signature": False, "verify_aud": False})
        return jwt_payload


class TipTapMixin:
    """Миксин для работы с редактором текста TipTap"""

    def __init__(self, client: AsyncClient):
        self.client = client

    async def get_tiptap_token(self, text_id: uuid.UUID) -> Token:
        """Получить токен для редактора текста TipTap"""
        response = await self.client.get(f"/tiptap/token/{text_id}")
        if response.status_code == 404:
            raise TextNotFoundError("Текст не найден")
        if response.status_code == 403:
            raise PermissionDeniedError("Недостаточно прав")
        return Token(**response.json())
