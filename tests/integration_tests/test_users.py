"""Интеграционные тесты работы с пользователями"""
import uuid

import pytest

from tests.integration_tests.test_client import LyricsClient
from tests.integration_tests.test_client.components.exceptions import PermissionDeniedError


@pytest.mark.asyncio
async def test_get_user_self(lyrics_client: LyricsClient):
    """Тест получения данных о себе"""
    assert lyrics_client.user_id is not None
    user = await lyrics_client.get_user(lyrics_client.user_id)
    assert user.user_id == lyrics_client.user_id
    assert user.email == lyrics_client.email


@pytest.mark.asyncio
async def test_get_user_other(lyrics_client: LyricsClient):
    """Тест получения данных другого пользователя"""
    with pytest.raises(PermissionDeniedError):
        await lyrics_client.get_user(uuid.uuid4())
