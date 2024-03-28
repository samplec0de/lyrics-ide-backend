import pytest
from httpx import AsyncClient
from app.api.schemas import Token

@pytest.mark.asyncio
async def test_get_tiptap_access_token(async_client: AsyncClient):
    response = await async_client.get("/tiptap/token")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data

@pytest.mark.asyncio
async def test_get_tiptap_access_token_v2(async_client: AsyncClient):
    response = await async_client.get("/tiptap/token/1")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
