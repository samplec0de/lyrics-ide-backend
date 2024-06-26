"""Интеграционные тесты для работы с токенами TipTap"""
import os
from datetime import datetime, timedelta

import pytest
from httpx import AsyncClient

from tests.integration_tests.test_client import LyricsClient
from tests.integration_tests.test_client.components.exceptions import PermissionDeniedError
from tests.integration_tests.test_client.components.projects import Project


@pytest.mark.asyncio
async def test_get_tiptap_token_owner(lyrics_client: LyricsClient, new_project: Project):
    """Тест получения токена для TipTap"""
    text = new_project.texts[0]
    token = await lyrics_client.get_tiptap_token(text.text_id)
    assert token
    assert token.token_type == "bearer"
    payload = await token.payload()
    assert payload["iat"] == payload["nbf"]
    assert datetime.utcnow() - datetime.fromtimestamp(payload["iat"]) < timedelta(seconds=5)
    assert payload["iss"] == "https://lyrics-backend.k8s-1.sslane.ru"
    assert payload["aud"] == os.getenv("TIPTAP_APP_ID")
    assert payload["allowedDocumentNames"] == [str(text.text_id)]
    assert payload["readonlyDocumentNames"] == []


@pytest.mark.asyncio
async def test_get_tiptap_token_read_only(
    lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project
):
    """Тест получения токена для TipTap с правами на чтение"""
    grant_code = await lyrics_client.get_project_share_code(new_project.project_id, "READ_ONLY", 1)
    await lyrics_client_b.activate_project_share_code(grant_code.grant_code_id)
    text = new_project.texts[0]
    token = await lyrics_client_b.get_tiptap_token(text.text_id)
    assert token
    assert token.token_type == "bearer"
    payload = await token.payload()
    assert payload["iat"] == payload["nbf"]
    assert datetime.utcnow() - datetime.fromtimestamp(payload["iat"]) < timedelta(seconds=5)
    assert payload["iss"] == "https://lyrics-backend.k8s-1.sslane.ru"
    assert payload["aud"] == os.getenv("TIPTAP_APP_ID")
    assert payload["allowedDocumentNames"] == [str(text.text_id)]
    assert payload["readonlyDocumentNames"] == [str(text.text_id)]


@pytest.mark.asyncio
async def test_get_tiptap_token_read_write(
    lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project
):
    """Тест получения токена для TipTap с правами на чтение"""
    grant_code = await lyrics_client.get_project_share_code(new_project.project_id, "READ_WRITE", 1)
    await lyrics_client_b.activate_project_share_code(grant_code.grant_code_id)
    text = new_project.texts[0]
    token = await lyrics_client_b.get_tiptap_token(text.text_id)
    assert token
    assert token.token_type == "bearer"
    payload = await token.payload()
    assert payload["iat"] == payload["nbf"]
    assert datetime.utcnow() - datetime.fromtimestamp(payload["iat"]) < timedelta(seconds=5)
    assert payload["iss"] == "https://lyrics-backend.k8s-1.sslane.ru"
    assert payload["aud"] == os.getenv("TIPTAP_APP_ID")
    assert payload["allowedDocumentNames"] == [str(text.text_id)]
    assert payload["readonlyDocumentNames"] == []


@pytest.mark.asyncio
async def test_get_tiptap_token_no_permissions(
    lyrics_client: LyricsClient, lyrics_client_b: LyricsClient, new_project: Project
):
    """Тест получения токена для TipTap без прав"""
    text = new_project.texts[0]
    with pytest.raises(PermissionDeniedError):
        await lyrics_client_b.get_tiptap_token(text.text_id)


@pytest.mark.asyncio
async def test_update_document_webhook(
    unauthorized_client: AsyncClient, lyrics_client: LyricsClient, new_project: Project
):
    """Тест обновления документа через webhook"""
    text = new_project.texts[0]
    tiptap_payload = {
        "name": str(text.text_id),
    }

    response = await unauthorized_client.post("/tiptap/webhook", json=tiptap_payload)

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

    updated_text = await lyrics_client.get_text(text.text_id)
    assert updated_text.updated_at > text.updated_at

    updated_project = await lyrics_client.get_project(new_project.project_id)
    assert updated_project.updated_at > new_project.updated_at
