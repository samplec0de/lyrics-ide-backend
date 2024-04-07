import uuid

from httpx import AsyncClient

from integration_tests.test_client.components.exceptions import PermissionDeniedError


class User:
    """Пользователь"""
    def __init__(self, user_id: str, email: str):
        self.user_id = uuid.UUID(user_id, version=4)
        self.email = email

    def __eq__(self, other):
        return self.user_id == other.user_id and self.email == other.email


class UserMixin:
    """Миксин для работы с пользователями"""

    def __init__(self, client: AsyncClient):
        self.client = client

    async def get_user(self, user_id: uuid.UUID) -> User:
        """Получить информацию о пользователе"""
        response = await self.client.get(f"/users/{user_id}")

        if response.status_code == 403:
            raise PermissionDeniedError("Пользователь не найден")

        return User(**response.json())
