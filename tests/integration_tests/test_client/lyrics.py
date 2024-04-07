from httpx import AsyncClient

from integration_tests.test_client.components.projects import ProjectsMixin


class LyricsClient(ProjectsMixin):
    """Тестовый клиент для Lyrics API"""

    def __init__(self, client: AsyncClient):
        self.client = client
        ProjectsMixin.__init__(self, client)
