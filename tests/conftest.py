from typing import AsyncIterator

import pytest

from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app as main_app
from app.database import get_db_session
from app.models import Base


DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(autocommit=False, bind=engine, expire_on_commit=False)
DBSession = AsyncSession


@pytest.fixture(scope="function", autouse=True)
async def db_session() -> AsyncIterator[AsyncSession]:
    async with TestingSessionLocal() as session:

        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
            await connection.commit()

        async def override_get_db_session():
            yield session

        main_app.dependency_overrides[get_db_session] = override_get_db_session
        yield session

        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client() -> AsyncClient:
    async with AsyncClient(app=main_app, base_url="http://test") as async_client:
        yield async_client
