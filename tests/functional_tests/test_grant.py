import pytest
from httpx import AsyncClient
from app.api.schemas import ProjectGrantCode, ProjectGrant

@pytest.mark.asyncio
async def test_get_project_share_code(async_client: AsyncClient):
    response = await async_client.get("/project/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, ProjectGrantCode)

@pytest.mark.asyncio
async def test_activate_project_share_code(async_client: AsyncClient):
    response = await async_client.get("/codes/activate/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, ProjectGrant)

@pytest.mark.asyncio
async def test_get_project_users(async_client: AsyncClient):
    response = await async_client.get("/project/1/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_revoke_project_access(async_client: AsyncClient):
    response = await async_client.delete("/1/users/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, ProjectGrant)

@pytest.mark.asyncio
async def test_get_project_codes(async_client: AsyncClient):
    response = await async_client.get("/projects/1/codes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_deactivate_project_grant_code(async_client: AsyncClient):
    response = await async_client.delete("/codes/1")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_project_access(async_client: AsyncClient):
    response = await async_client.patch("/1/users/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, ProjectGrant)

@pytest.mark.asyncio
async def test_leave_project(async_client: AsyncClient):
    response = await async_client.delete("/1/leave")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, ProjectGrant)
