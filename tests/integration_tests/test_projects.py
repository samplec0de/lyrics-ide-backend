import uuid

import pytest

from integration_tests.test_client import LyricsClient
from integration_tests.test_client.components.exceptions import PermissionDeniedError, ProjectNotFoundError
from integration_tests.test_client.components.projects import Project


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


@pytest.mark.parametrize("name, description", [
    ("Updated project", "Updated description"),
    (None, "Updated description"),
    ("Updated project", None),
])
@pytest.mark.asyncio
async def test_update_project(name: str | None, description: str | None, lyrics_client: LyricsClient):
    project = await lyrics_client.create_project("Test project", "Test description")
    updated_project = await lyrics_client.update_project(project.project_id, name, description)
    assert updated_project.name == name or "Test project"
    assert updated_project.description == description or "Test description"
    assert updated_project.owner_user_id is not None
    assert updated_project.is_owner is True
    assert updated_project.grant_level is None
    assert len(updated_project.texts) == 1
    assert updated_project.music is None
    assert updated_project.created_at is not None
    assert updated_project.updated_at is not None


@pytest.mark.asyncio
async def test_delete_project(lyrics_client: LyricsClient):
    project = await lyrics_client.create_project("Test project", "Test description")
    await lyrics_client.delete_project(project.project_id)
    with pytest.raises(ProjectNotFoundError):
        await lyrics_client.get_project(project.project_id)


@pytest.mark.asyncio
async def test_delete_project_with_grant(
        lyrics_client: LyricsClient,
        new_project: Project,
        lyrics_client_b: LyricsClient
):
    grant_code = await lyrics_client.get_project_share_code(
        new_project.project_id, "READ_WRITE", 1
    )
    await lyrics_client_b.activate_project_share_code(grant_code.grant_code_id)
    await lyrics_client.delete_project(new_project.project_id)
    with pytest.raises(ProjectNotFoundError):
        await lyrics_client.get_project(new_project.project_id)


@pytest.mark.asyncio
async def test_delete_project_not_found(lyrics_client: LyricsClient):
    with pytest.raises(ProjectNotFoundError):
        await lyrics_client.delete_project(uuid.uuid4())


@pytest.mark.asyncio
async def test_delete_project_not_owner(lyrics_client: LyricsClient, lyrics_client_b: LyricsClient):
    project = await lyrics_client.create_project("Test project", "Test description")
    with pytest.raises(PermissionDeniedError):
        await lyrics_client_b.delete_project(project.project_id)


@pytest.mark.asyncio
async def test_get_project(lyrics_client: LyricsClient):
    project = await lyrics_client.create_project("Test project", "Test description")
    got_project = await lyrics_client.get_project(project.project_id)
    assert got_project.name == "Test project"
    assert got_project.description == "Test description"
    assert got_project.owner_user_id is not None
    assert got_project.is_owner is True
    assert got_project.grant_level is None
    assert len(got_project.texts) == 1
    assert got_project.music is None
    assert got_project.created_at is not None
    assert got_project.updated_at is not None


@pytest.mark.asyncio
async def test_get_project_not_found(lyrics_client: LyricsClient):
    with pytest.raises(ProjectNotFoundError):
        await lyrics_client.get_project(uuid.uuid4())


@pytest.mark.asyncio
async def test_get_projects_empty(lyrics_client: LyricsClient):
    projects = await lyrics_client.get_projects()
    assert len(projects) == 0


@pytest.mark.asyncio
async def test_get_projects(lyrics_client: LyricsClient):
    project1 = await lyrics_client.create_project("Test project 1", "Test description 1")
    project2 = await lyrics_client.create_project("Test project 2", "Test description 2")
    projects = await lyrics_client.get_projects()
    assert len(projects) == 2
    assert project1 in projects
    assert project2 in projects
