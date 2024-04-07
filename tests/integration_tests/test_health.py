from unittest.mock import patch, AsyncMock

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_liveness(unauthorized_client: AsyncClient):
    response = await unauthorized_client.get("/health/liveness")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


@pytest.mark.asyncio
async def test_health_check_readiness(unauthorized_client: AsyncClient):
    response = await unauthorized_client.get("/health/readiness")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


@pytest.mark.asyncio
@patch("sqlalchemy.ext.asyncio.AsyncSession.execute", new_callable=AsyncMock)
async def test_health_check_readiness_error(mock_execute, unauthorized_client: AsyncClient):
    # with  as mock_execute:
    mock_execute.side_effect = Exception("DB Error")
    response = await unauthorized_client.get("/health/readiness")
    assert response.status_code == 503
