"""Интеграционные тесты CRUD текстов"""
import uuid

import pytest

from tests.integration_tests.test_client import LyricsClient
from tests.integration_tests.test_client.components.exceptions import (
    TextNotFoundError,
    UnAuthorizedError,
    PermissionDeniedError,
)
from tests.integration_tests.test_client.components.projects import Project


@pytest.mark.asyncio
async def test_create_text(lyrics_client: LyricsClient, new_project: Project):
    """Тест создания текста"""
    text = await lyrics_client.create_text(new_project.project_id, "Test text")
    assert text.name == "Test text"
    assert isinstance(text.text_id, uuid.UUID)


@pytest.mark.asyncio
async def test_get_text(lyrics_client: LyricsClient, new_project: Project):
    """Тест получения текста"""
    text = await lyrics_client.create_text(new_project.project_id, "Test text")
    got_text = await lyrics_client.get_text(text.text_id)
    assert got_text == text


@pytest.mark.asyncio
async def test_get_text_not_found(lyrics_client: LyricsClient):
    """Тест получения несуществующего текста"""
    with pytest.raises(TextNotFoundError):
        await lyrics_client.get_text(uuid.uuid4())


@pytest.mark.asyncio
async def test_get_text_unauthorized(unauthorized_client):
    """Тест получения текста без авторизации"""
    with pytest.raises(UnAuthorizedError):
        await LyricsClient(client=unauthorized_client, email=None, user_id=None).get_text(uuid.uuid4())


@pytest.mark.asyncio
async def test_get_text_forbidden(new_project: Project, lyrics_client_b: LyricsClient):
    """Тест получения текста без прав"""
    text = new_project.texts[0]
    with pytest.raises(PermissionDeniedError):
        await lyrics_client_b.get_text(text.text_id)


@pytest.mark.asyncio
async def test_update_text(lyrics_client: LyricsClient, new_project: Project):
    """Тест обновления текста"""
    text = new_project.texts[0]
    new_text = await lyrics_client.update_text(text.text_id, "New text")
    assert new_text.name == "New text"
    assert new_text.text_id == text.text_id


@pytest.mark.asyncio
async def test_update_text_unchanged(lyrics_client: LyricsClient, new_project: Project):
    """Тест обновления текста без изменений"""
    text = new_project.texts[0]
    new_text = await lyrics_client.update_text(text.text_id, name=None)
    assert new_text.name == text.name
    assert new_text.text_id == text.text_id


@pytest.mark.asyncio
async def test_update_text_unauthorized(unauthorized_client, new_project: Project):
    """Тест обновления текста без авторизации"""
    text = new_project.texts[0]
    with pytest.raises(UnAuthorizedError):
        unauthorized_lyrics_client = LyricsClient(client=unauthorized_client, email=None, user_id=None)
        await unauthorized_lyrics_client.update_text(text.text_id, "New text")


@pytest.mark.asyncio
async def test_update_text_forbidden(new_project: Project, lyrics_client_b: LyricsClient):
    """Тест обновления текста без прав"""
    text = new_project.texts[0]
    with pytest.raises(PermissionDeniedError):
        await lyrics_client_b.update_text(text.text_id, "New text")


@pytest.mark.asyncio
async def test_delete_single_text(lyrics_client: LyricsClient, new_project: Project):
    """Тест удаления единственного текста"""
    text = new_project.texts[0]
    with pytest.raises(PermissionDeniedError):
        await lyrics_client.delete_text(text.text_id)


@pytest.mark.asyncio
async def test_delete_text(lyrics_client: LyricsClient, new_project: Project):
    """Тест удаления текста"""
    await lyrics_client.create_text(new_project.project_id, "Test text 2")
    text = new_project.texts[0]
    await lyrics_client.delete_text(text.text_id)
    with pytest.raises(TextNotFoundError):
        await lyrics_client.get_text(text.text_id)


@pytest.mark.asyncio
async def test_delete_text_unauthorized(unauthorized_client, new_project: Project):
    """Тест удаления текста без авторизации"""
    text = new_project.texts[0]
    with pytest.raises(UnAuthorizedError):
        unauthorized_lyrics_client = LyricsClient(client=unauthorized_client, email=None, user_id=None)
        await unauthorized_lyrics_client.delete_text(text.text_id)


@pytest.mark.asyncio
async def test_delete_text_forbidden(new_project: Project, lyrics_client_b: LyricsClient):
    """Тест удаления текста без прав"""
    await lyrics_client_b.create_text(new_project.project_id, "Test text 2")
    text = new_project.texts[0]
    with pytest.raises(PermissionDeniedError):
        await lyrics_client_b.delete_text(text.text_id)
