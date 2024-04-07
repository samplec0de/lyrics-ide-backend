import datetime
import uuid

from httpx import AsyncClient

from integration_tests.test_client.components.grants import GrantLevel
from integration_tests.test_client.components.music import Music
from integration_tests.test_client.components.text import Text


class Project:
    """Проект"""
    def __init__(
            self,
            project_id: uuid.UUID,
            name: str,
            description: str,
            owner_user_id: uuid.UUID,
            is_owner: bool,
            grant_level: GrantLevel | None,
            created_at: datetime.datetime,
            updated_at: datetime.datetime,
            texts: list[dict],
            music: Music | None,
    ):
        self.project_id = project_id
        self.name = name
        self.description = description
        self.owner_user_id = owner_user_id
        self.is_owner = is_owner
        self.grant_level = grant_level
        self.created_at = created_at
        self.updated_at = updated_at
        self.texts = [
            Text(
                text_id=text["text_id"],
                project_id=project_id,
                created_at=text["created_at"],
                updated_at=text["updated_at"],
            )
            for text in texts
        ]
        self.music = Music(
            url=music.url,
            duration_seconds=music.duration_seconds,
            bpm=music.bpm,
            custom_bpm=music.custom_bpm,
        ) if music else None


class ProjectsMixin:
    def __init__(self, client: AsyncClient):
        self.client = client

    async def create_project(self, name: str, description: str) -> Project:
        response = await self.client.post(
            "/projects/",
            json={"name": name, "description": description},
        )
        return Project(**response.json())
