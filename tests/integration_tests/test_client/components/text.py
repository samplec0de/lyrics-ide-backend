"""Компонент для работы с текстами"""
import datetime
import uuid

from httpx import AsyncClient

from tests.integration_tests.test_client.components.exceptions import (
    TextNotFoundError,
    UnAuthorizedError,
    PermissionDeniedError,
)


class Text:
    """Текст"""

    def __init__(
        self,
        text_id: str,
        name: str | None,
        created_at: datetime.datetime,
        updated_at: datetime.datetime,
        **_,
    ):
        self.text_id = uuid.UUID(text_id, version=4)
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    def __eq__(self, other):
        return (
            self.text_id == other.text_id
            and self.created_at == other.created_at
            and self.updated_at == other.updated_at
        )


class TextMixin:
    """Миксин для текста"""

    def __init__(self, client: AsyncClient):
        self.client = client

    async def create_text(self, project_id: uuid.UUID, name: str | None) -> Text:
        """Создать текст"""
        payload = {"project_id": str(project_id)}
        if name is not None:
            payload["name"] = name

        response = await self.client.post(
            "/texts/",
            json=payload,
        )
        response.raise_for_status()
        return Text(**response.json())

    async def get_text(self, text_id: uuid.UUID) -> Text:
        """Получить текст"""
        response = await self.client.get(f"/texts/{text_id}")

        if response.status_code == 404:
            raise TextNotFoundError("Text not found")
        if response.status_code == 401:
            raise UnAuthorizedError("Unauthorized")
        if response.status_code == 403:
            raise PermissionDeniedError("Permission denied")

        return Text(**response.json())

    async def update_text(self, text_id: uuid.UUID, name: str | None) -> Text:
        """Обновить текст"""
        payload = {}
        if name is not None:
            payload["name"] = name

        response = await self.client.patch(
            f"/texts/{text_id}",
            json=payload,
        )

        if response.status_code == 404:
            raise TextNotFoundError("Text not found")
        if response.status_code == 401:
            raise UnAuthorizedError("Unauthorized")
        if response.status_code == 403:
            raise PermissionDeniedError("Permission denied")

        return Text(**response.json())

    async def delete_text(self, text_id: uuid.UUID) -> None:
        """Удалить текст"""
        response = await self.client.delete(f"/texts/{text_id}")

        if response.status_code == 404:
            raise TextNotFoundError("Text not found")
        if response.status_code == 401:
            raise UnAuthorizedError("Unauthorized")
        if response.status_code == 403:
            raise PermissionDeniedError("Permission denied")
        response.raise_for_status()
