import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_project(async_client: AsyncClient):
    project_data = {"name": "Test Project", "description": "This is a test project"}
    response = await async_client.post("/project/", json=project_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == project_data["name"]
    assert data["description"] == project_data["description"]


@pytest.mark.asyncio
async def test_update_project(async_client: AsyncClient):
    project_data = {"name": "Updated Project", "description": "This is an updated test project"}
    response = await async_client.patch("/project/1", json=project_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == project_data["name"]
    assert data["description"] == project_data["description"]


@pytest.mark.asyncio
async def test_get_projects(async_client: AsyncClient):
    response = await async_client.get("/project/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_project(async_client: AsyncClient):
    response = await async_client.get("/project/1")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "description" in data


@pytest.mark.asyncio
async def test_delete_project(async_client: AsyncClient):
    response = await async_client.delete("/project/1")
    assert response.status_code == 200
