"""Модуль для работы с БД"""
import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.config import settings


Base = declarative_base()

# Heavily inspired by https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html


class DatabaseSessionManager:
    """Менеджер сессий БД"""

    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None):
        """Инициализация менеджера сессий к БД"""
        if engine_kwargs is None:
            engine_kwargs = {}
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine, expire_on_commit=False)

    async def close(self):
        """Закрытие соединения с БД"""
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """Подключение к БД"""
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Сессия для работы с БД"""

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(settings.database_url, {"echo": settings.echo_sql})


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """Сессия для работы с БД"""
    async with sessionmanager.session() as session:
        yield session
