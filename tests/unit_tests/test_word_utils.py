# file: test_word_utils.py
import pytest
from unittest.mock import AsyncMock
import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from app.word_utils import get_word_meanings, get_synonyms


@pytest.fixture
def mock_db_session():
    """Fixture to mock the async database session."""

    class MockSession(AsyncSession):
        async def execute(self, query):
            # Mock the database response based on the query
            class MockResult:
                def scalars(self):
                    return [MockWordMeaning("meaning1"), MockWordMeaning("meaning2")]

            return MockResult()

    return MockSession()


class MockWordMeaning:
    """Mock class for WordMeaningModel results."""

    def __init__(self, meaning):
        self.meaning = meaning


@pytest.mark.asyncio
async def test_get_word_meanings_existing_word(mock_db_session):
    word = "Test"
    expected_meanings = ["meaning1", "meaning2"]
    meanings = await get_word_meanings(word, mock_db_session)
    assert meanings == expected_meanings


@pytest.mark.asyncio
async def test_get_synonyms_with_mocked_api_response(mocker):
    class MockResponse:
        status = 200

        async def json(self):
            return {
                "def": [
                    {"tr": [{"text": "synonym1"}, {"text": "synonym2"}]}
                ]
            }

    class MockPost:
        async def __aenter__(self):
            return MockResponse()

        async def __aexit__(self, exc_type, exc, tb):
            pass

    mocker.patch('aiohttp.ClientSession.post', return_value=MockPost())

    word = "Test"
    expected_synonyms = ["synonym1", "synonym2"]
    synonyms = await get_synonyms(word)
    assert synonyms == expected_synonyms


@pytest.mark.asyncio
async def test_get_synonyms_with_mocked_api_response_negative(mocker):
    class MockResponse:
        status = 404

    class MockPost:
        async def __aenter__(self):
            return MockResponse()

        async def __aexit__(self, exc_type, exc, tb):
            pass

    mocker.patch('aiohttp.ClientSession.post', return_value=MockPost())

    word = "Test"
    expected_synonyms = []
    synonyms = await get_synonyms(word)
    assert synonyms == expected_synonyms
