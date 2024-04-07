import uuid

import pytest

from integration_tests.test_client import LyricsClient
from integration_tests.test_client.components.exceptions import PermissionDeniedError


@pytest.mark.asyncio
async def test_get_user_self(lyrics_client: LyricsClient):
    user = await lyrics_client.get_user(lyrics_client.user_id)
    assert user.user_id == lyrics_client.user_id
    assert user.email == lyrics_client.email


@pytest.mark.asyncio
async def test_get_user_other(lyrics_client: LyricsClient):
    with pytest.raises(PermissionDeniedError):
        await lyrics_client.get_user(uuid.uuid4())
