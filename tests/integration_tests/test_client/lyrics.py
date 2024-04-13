"""Тестовый клиент для Lyrics API"""
import uuid

from httpx import AsyncClient

from tests.integration_tests.test_client.components.grants import GrantMixin
from tests.integration_tests.test_client.components.music import MusicMixin
from tests.integration_tests.test_client.components.projects import ProjectsMixin
from tests.integration_tests.test_client.components.text import TextMixin
from tests.integration_tests.test_client.components.tiptap import TipTapMixin
from tests.integration_tests.test_client.components.user import UserMixin


class LyricsClient(ProjectsMixin, TextMixin, UserMixin, GrantMixin, MusicMixin, TipTapMixin):
    """Тестовый клиент для Lyrics API"""

    def __init__(self, user_id: uuid.UUID | None, email: str | None, client: AsyncClient):
        self.client = client
        self.user_id = user_id
        self.email = email

        ProjectsMixin.__init__(self, client)
        TextMixin.__init__(self, client)
        UserMixin.__init__(self, client)
        GrantMixin.__init__(self, client)
        MusicMixin.__init__(self, client)
        TipTapMixin.__init__(self, client)
