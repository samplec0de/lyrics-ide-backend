import uuid

from httpx import AsyncClient

from integration_tests.test_client.components.exceptions import MusicNotFoundError, ProjectNotFoundError, \
    PermissionDeniedError


class Music:
    """Музыка"""
    def __init__(
            self,
            url: str,
            duration_seconds: float,
            bpm: int | None,
            custom_bpm: int | None,
    ):
        self.url = url
        self.duration_seconds = duration_seconds
        self.bpm = bpm
        self.custom_bpm = custom_bpm


class MusicMixin:
    """Миксин для работы с музыкой"""
    def __init__(self, client: AsyncClient):
        self.client = client

    async def upload_music(self, file_path: str, project_id: uuid.UUID) -> Music:
        """Загрузить музыку"""
        response = await self.client.post(
            f"/music/{project_id}",
            files={"music": open(file_path, "rb")},
        )
        if response.status_code == 404:
            raise ProjectNotFoundError("Проект не найден")
        elif response.status_code == 403:
            raise PermissionDeniedError("Недостаточно прав")
        return Music(**response.json())

    async def get_music(self, project_id: uuid.UUID) -> Music:
        """Получить музыку"""
        response = await self.client.get(f"/music/{project_id}")
        if response.status_code == 400:
            raise MusicNotFoundError("Музыка не найдена")
        if response.status_code == 404:
            raise ProjectNotFoundError("Проект не найден")
        if response.status_code == 403:
            raise PermissionDeniedError("Недостаточно прав")
        return Music(**response.json())

    async def set_music_custom_bpm(self, project_id: uuid.UUID, bpm: int) -> Music:
        """Установить BPM у музыки"""
        response = await self.client.patch(f"/music/{project_id}", params={"custom_bpm": bpm})
        if response.status_code == 400:
            raise MusicNotFoundError("Музыка не найдена")
        if response.status_code == 404:
            raise ProjectNotFoundError("Проект не найден")
        return Music(**response.json())
