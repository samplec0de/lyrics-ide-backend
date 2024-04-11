import datetime
import uuid

from httpx import AsyncClient

from integration_tests.test_client.components.exceptions import PermissionDeniedError, UnAuthorizedError, \
    ProjectNotFoundError, MusicNotFoundError
from integration_tests.test_client.components.grant_level import GrantLevel
from integration_tests.test_client.components.music import Music
from integration_tests.test_client.components.text import Text


class Project:
    """Проект"""
    def __init__(
            self,
            project_id: str,
            name: str,
            description: str,
            owner_user_id: str,
            is_owner: bool,
            grant_level: GrantLevel | None,
            created_at: datetime.datetime,
            updated_at: datetime.datetime,
            texts: list[dict],
            music: dict | None,
    ):
        self.project_id = uuid.UUID(project_id, version=4)
        self.name = name
        self.description = description
        self.owner_user_id = uuid.UUID(owner_user_id, version=4)
        self.is_owner = is_owner
        self.grant_level = grant_level
        self.created_at = created_at
        self.updated_at = updated_at
        self.texts = [
            Text(
                text_id=text["text_id"],
                project_id=project_id,
                name=text["name"],
                created_at=text["created_at"],
                updated_at=text["updated_at"],
            )
            for text in texts
        ]
        self.music = Music(
            url=music["url"],
            duration_seconds=music["duration_seconds"],
            bpm=music["bpm"],
            custom_bpm=music["custom_bpm"],
        ) if music else None

    def __eq__(self, other):
        return (
            self.project_id == other.project_id
            and self.name == other.name
            and self.description == other.description
            and self.owner_user_id == other.owner_user_id
            and self.is_owner == other.is_owner
            and self.grant_level == other.grant_level
            and self.created_at == other.created_at
            and self.updated_at == other.updated_at
            and self.texts == other.texts
            and self.music == other.music
        )


class ProjectsMixin:
    def __init__(self, client: AsyncClient):
        self.client = client

    async def create_project(self, name: str, description: str) -> Project:
        """Создать проект"""
        response = await self.client.post(
            "/projects/",
            json={"name": name, "description": description},
        )
        return Project(**response.json())

    async def get_project(self, project_id: uuid.UUID) -> Project:
        """Получить проект по идентификатору"""
        response = await self.client.get(f"/projects/{project_id}")
        if response.status_code == 404:
            raise ProjectNotFoundError("Проект не найден")
        return Project(**response.json())

    async def delete_project(self, project_id: uuid.UUID) -> None:
        """Удалить проект по идентификатору"""
        response = await self.client.delete(f"/projects/{project_id}")
        if response.status_code == 404:
            raise ProjectNotFoundError("Проект не найден")
        if response.status_code == 401:
            raise UnAuthorizedError("Unauthorized")
        if response.status_code == 403:
            raise PermissionDeniedError("Permission denied")

    async def get_projects(self) -> list[Project]:
        """Получить список проектов"""
        response = await self.client.get("/projects/")
        return [Project(**project) for project in response.json()]

    async def update_project(self, project_id: uuid.UUID, name: str, description: str) -> Project:
        """Обновить проект"""
        payload = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description

        response = await self.client.patch(
            f"/projects/{project_id}",
            json=payload,
        )
        return Project(**response.json())

    async def delete_music(self, project_id: uuid.UUID) -> Project:
        """Удалить музыку"""
        response = await self.client.delete(f"/music/{project_id}")
        if response.status_code == 400:
            raise MusicNotFoundError("Музыка не найдена")
        if response.status_code == 404:
            raise ProjectNotFoundError("Проект не найден")
        if response.status_code == 403:
            raise PermissionDeniedError("Недостаточно прав")
        return Project(**response.json())
