"""Тесты для проверки готовности сервиса"""
from unittest.mock import patch, AsyncMock

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_liveness(unauthorized_client: AsyncClient):
    """Тест проверки живучести сервиса без ошибок"""
    response = await unauthorized_client.get("/health/liveness")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


@pytest.mark.asyncio
async def test_health_check_readiness(unauthorized_client: AsyncClient):
    """Тест проверки готовности сервиса без ошибок"""
    response = await unauthorized_client.get("/health/readiness")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


@pytest.mark.asyncio
@patch("sqlalchemy.ext.asyncio.AsyncSession.execute", new_callable=AsyncMock)
async def test_health_check_readiness_error(mock_execute, unauthorized_client: AsyncClient):
    """Тест проверки готовности сервиса с ошибкой"""
    mock_execute.side_effect = Exception("DB Error")
    response = await unauthorized_client.get("/health/readiness")
    assert response.status_code == 503
