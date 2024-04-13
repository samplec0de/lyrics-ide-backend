"""Фикстуры для тестов"""
import uuid
from typing import AsyncIterator, AsyncGenerator

import pytest

from httpx import AsyncClient
from jose import jwt
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.auth import get_new_email_auth_code
from app.main import app as main_app
from app.database import get_db_session
from app.models import Base, EmailAuthCodeModel

from tests.integration_tests.test_client.lyrics import LyricsClient

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
EMAIL = "test@lirix.xyz"
EMAIL_B = "test_b@lirix.xyz"


@pytest.fixture(name="db_session", scope="function", autouse=True)
async def db_session_fixture() -> AsyncIterator[AsyncSession]:
    """Сессия базы данных для тестов"""
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


@pytest.fixture(name="unauthorized_client", scope="function")
async def client_fixture() -> AsyncGenerator[AsyncClient, None]:
    """Клиент для тестов"""
    async with AsyncClient(app=main_app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture(name="authorized_client", scope="function")
async def authorized_client_fixture(db_session: DBSession):
    """Авторизованный клиент"""
    new_code = await get_new_email_auth_code()
    new_code_model = EmailAuthCodeModel(email=EMAIL, auth_code=new_code)
    db_session.add(new_code_model)
    await db_session.commit()

    async with AsyncClient(app=main_app, base_url="http://test") as async_client:
        response = await async_client.post(
            "/auth/token",
            data={"username": EMAIL, "password": new_code},
        )
        access_token = response.json()["access_token"]
        async_client.headers["Authorization"] = f"Bearer {access_token}"
        yield async_client


@pytest.fixture(name="authorized_client_b", scope="function")
async def authorized_client_b_fixture(db_session: DBSession):
    """Авторизованный клиент с другим пользователем"""
    new_code = await get_new_email_auth_code()
    new_code_model = EmailAuthCodeModel(email=EMAIL_B, auth_code=new_code)
    db_session.add(new_code_model)
    await db_session.commit()

    async with AsyncClient(app=main_app, base_url="http://test") as async_client:
        response = await async_client.post(
            "/auth/token",
            data={"username": EMAIL_B, "password": new_code},
        )
        access_token = response.json()["access_token"]
        async_client.headers["Authorization"] = f"Bearer {access_token}"
        yield async_client


@pytest.fixture(name="lyrics_client", scope="function")
async def lyrics_client_fixture(authorized_client: AsyncClient):
    """Клиент для тестов"""
    jwt_token = authorized_client.headers["Authorization"].split(" ")[1]
    jwt_payload = jwt.decode(jwt_token, "", options={"verify_signature": False})
    user_id = uuid.UUID(jwt_payload["user_id"], version=4)
    email = jwt_payload["sub"]
    return LyricsClient(user_id=user_id, email=email, client=authorized_client)


@pytest.fixture(name="lyrics_client_b", scope="function")
async def lyrics_client_b_fixture(authorized_client_b: AsyncClient):
    """Клиент для тестов с другим пользователем"""
    jwt_token = authorized_client_b.headers["Authorization"].split(" ")[1]
    jwt_payload = jwt.decode(jwt_token, "", options={"verify_signature": False})
    user_id = uuid.UUID(jwt_payload["user_id"], version=4)
    email = jwt_payload["sub"]
    return LyricsClient(user_id=user_id, email=email, client=authorized_client_b)


@pytest.fixture(name="new_project", scope="function")
async def new_project_fixture(lyrics_client: LyricsClient):
    """Создает новый проект для тестов"""
    project = await lyrics_client.create_project(name="Test project", description="Test description")
    return project
