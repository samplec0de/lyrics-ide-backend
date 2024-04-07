import uuid

from httpx import AsyncClient

from integration_tests.test_client.components.projects import ProjectsMixin
from integration_tests.test_client.components.user import UserMixin


class LyricsClient(ProjectsMixin, UserMixin):
    """Тестовый клиент для Lyrics API"""

    def __init__(self, user_id: uuid.UUID, email: str, client: AsyncClient):
        self.client = client
        self.user_id = user_id
        self.email = email

        ProjectsMixin.__init__(self, client)
        UserMixin.__init__(self, client)
