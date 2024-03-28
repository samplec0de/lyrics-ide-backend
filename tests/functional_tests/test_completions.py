import pytest
from httpx import AsyncClient
from app.api.schemas import CompletionIn

@pytest.mark.asyncio
async def test_create_completion(async_client: AsyncClient):
    completion_data = {"text": "Test completion"}
    response = await async_client.post("/completions/", json=completion_data)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("completion" in completion for completion in data)
