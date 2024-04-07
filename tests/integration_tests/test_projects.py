import pytest

from integration_tests.test_client import LyricsClient


@pytest.mark.asyncio
async def test_create_project(lyrics_client: LyricsClient):
    project = await lyrics_client.create_project("Test project", "Test description")
    assert project.name == "Test project"
    assert project.description == "Test description"
    assert project.owner_user_id is not None
    assert project.is_owner is True
    assert project.grant_level is None
    assert len(project.texts) == 1
    assert project.music is None
    assert project.created_at is not None
    assert project.updated_at is not None
