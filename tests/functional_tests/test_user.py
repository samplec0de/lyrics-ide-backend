import pytest
from httpx import AsyncClient
from app.api.schemas import UserOut

@pytest.mark.asyncio
async def test_get_user(async_client: AsyncClient):
    response = await async_client.get("/user/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, UserOut)
