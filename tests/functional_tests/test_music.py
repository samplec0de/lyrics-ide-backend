import pytest
from httpx import AsyncClient
from app.api.schemas import MusicIn, MusicOut, ProjectOut

@pytest.mark.asyncio
async def test_upload_music(async_client: AsyncClient):
    music_data = {"file": "test_music_file.mp3"}
    response = await async_client.post("/music/1", files=music_data)
    assert response.status_code == 200
    data = response.json()
    assert data["url"] is not None
    assert data["duration_seconds"] is not None
    assert data["bpm"] is not None

@pytest.mark.asyncio
async def test_get_music(async_client: AsyncClient):
    response = await async_client.get("/music/1")
    assert response.status_code == 200
    data = response.json()
    assert data["url"] is not None
    assert data["duration_seconds"] is not None
    assert data["bpm"] is not None

@pytest.mark.asyncio
async def test_set_music_bpm(async_client: AsyncClient):
    bpm_data = {"custom_bpm": 120}
    response = await async_client.patch("/music/1", json=bpm_data)
    assert response.status_code == 200
    data = response.json()
    assert data["custom_bpm"] == bpm_data["custom_bpm"]

@pytest.mark.asyncio
async def test_delete_music(async_client: AsyncClient):
    response = await async_client.delete("/music/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, ProjectOut)
