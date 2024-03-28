import pytest
from httpx import AsyncClient
from app.api.schemas import WordMeaning

@pytest.mark.asyncio
async def test_get_word_meanings(async_client: AsyncClient):
    response = await async_client.get("/word/meaning?word=test")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(isinstance(item, WordMeaning) for item in data)

@pytest.mark.asyncio
async def test_get_word_synonyms(async_client: AsyncClient):
    response = await async_client.get("/word/synonyms?word=test")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_word_rhyming(async_client: AsyncClient):
    response = await async_client.get("/word/rhyming?word=test")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
