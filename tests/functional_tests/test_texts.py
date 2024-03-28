import pytest
from httpx import AsyncClient
from app.api.schemas import TextVariantIn, TextVariantWithoutID

@pytest.mark.asyncio
async def test_create_text(async_client: AsyncClient):
    text_data = {"project_id": "test_project_id", "name": "Test Text"}
    response = await async_client.post("/text/", json=text_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == text_data["name"]

@pytest.mark.asyncio
async def test_get_text(async_client: AsyncClient):
    response = await async_client.get("/text/1")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data

@pytest.mark.asyncio
async def test_update_text(async_client: AsyncClient):
    text_data = {"name": "Updated Text"}
    response = await async_client.patch("/text/1", json=text_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == text_data["name"]

@pytest.mark.asyncio
async def test_delete_text(async_client: AsyncClient):
    response = await async_client.delete("/text/1")
    assert response.status_code == 200
