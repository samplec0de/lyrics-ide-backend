"""Юнит-тесты word_utils.py"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.word_utils import get_word_meanings, get_synonyms


@pytest.fixture(name="mock_db_session")
def mock_db_session_fixture():
    """Fixture to mock the async database session."""

    class MockSession(AsyncSession):
        """Мок для сессии базы данных"""

        @classmethod
        def _no_async_engine_events(cls):
            """Мок для метода _no_async_engine_events"""

        async def execute(self, query, *args, **kwargs):  # pylint: disable=arguments-differ
            """Мок для выполнения запроса к базе данных"""

            class MockResult:
                """Мок для результата запроса к базе данных"""

                def scalars(self):
                    """Мок для метода scalars() результата запроса к базе данных"""
                    return [MockWordMeaning("meaning1"), MockWordMeaning("meaning2")]

            return MockResult()

    return MockSession()


class MockWordMeaning:
    """Mock class for WordMeaningModel results."""

    def __init__(self, meaning):
        self.meaning = meaning


@pytest.mark.asyncio
async def test_get_word_meanings_existing_word(mock_db_session):
    """Тест на получение значений слова из базы данных."""
    word = "Test"
    expected_meanings = ["meaning1", "meaning2"]
    meanings = await get_word_meanings(word, mock_db_session)
    assert meanings == expected_meanings


@pytest.mark.asyncio
async def test_get_synonyms_with_mocked_api_response(mocker):
    """Тест на получение синонимов с мокнутым ответом от API"""

    class MockResponse:
        """Мок aiohttp.ClientResponse"""

        status = 200

        async def json(self):
            """Мок метода json() для aiohttp.ClientResponse"""
            return {"def": [{"tr": [{"text": "synonym1"}, {"text": "synonym2"}]}]}

    class MockPost:
        """Мок aiohttp.ClientSession.post"""

        async def __aenter__(self):
            return MockResponse()

        async def __aexit__(self, exc_type, exc, traceback):
            """Мок метода __aexit__ для aiohttp.ClientSession.post"""

    mocker.patch("aiohttp.ClientSession.post", return_value=MockPost())

    word = "Test"
    expected_synonyms = ["synonym1", "synonym2"]
    synonyms = await get_synonyms(word)
    assert synonyms == expected_synonyms


@pytest.mark.asyncio
async def test_get_synonyms_with_mocked_api_response_negative(mocker):
    """Тест на получение синонимов с мокнутым ответом от API при отсутствии синонимов"""

    class MockResponse:
        """Мок aiohttp.ClientResponse"""

        status = 404

    class MockPost:
        """Мок aiohttp.ClientSession.post"""

        async def __aenter__(self):
            return MockResponse()

        async def __aexit__(self, exc_type, exc, traceback):
            pass

    mocker.patch("aiohttp.ClientSession.post", return_value=MockPost())

    word = "Test"
    expected_synonyms = []
    synonyms = await get_synonyms(word)
    assert synonyms == expected_synonyms
