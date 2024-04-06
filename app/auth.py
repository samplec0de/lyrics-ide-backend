import random
import uuid
from typing import Annotated, cast

import aiohttp
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, UUID4
import datetime
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy import select, ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencies.core import DBSessionDep
from app.api.schemas import UserOut
from app.config import settings
from app.models import UserModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    user_id: UUID4


ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(data: dict, secret_key: str = settings.secret_key):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=settings.token_expire_days)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception


async def validate_yandex_token(yandex_oauth: str):
    """Проверка токена Яндекса"""
    yandex_id_secret_key = settings.yandex_id_secret_key
    try:
        headers = {"Authorization": f"OAuth {yandex_oauth}"}
        async with aiohttp.ClientSession() as session:
            async with session.get('https://login.yandex.ru/info?format=jwt', headers=headers) as resp:
                yandex_jwt = await resp.text()
                payload = jwt.decode(yandex_jwt, yandex_id_secret_key, algorithms=["HS256"])
                return payload
    except ExpiredSignatureError:
        return None
    except JWTError:
        return None


async def create_user_if_not_exists(email: str, db_session: AsyncSession) -> UserModel:
    """Добавляет пользователя в базу данных если его там нет"""
    user_query = await db_session.execute(
        select(UserModel)
        .where(cast(ColumnElement[bool], UserModel.email == email))
    )
    user = user_query.scalars().first()
    if user is None:
        user = UserModel(email=email)
        db_session.add(user)
        return user
    else:
        return user


async def check_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ошибка проверки ключа доступа",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("user_id")
        if username is None or not isinstance(username, str) or user_id is None or not isinstance(user_id, str):
            raise credentials_exception
        token_data = TokenData(username=username, user_id=uuid.UUID(user_id, version=4))
    except JWTError:
        raise credentials_exception
    user = UserOut(email=token_data.username, user_id=token_data.user_id)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db_session: DBSessionDep) -> UserModel | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ошибка проверки ключа доступа",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("user_id")
        if username is None or not isinstance(username, str) or user_id is None or not isinstance(user_id, str):
            raise credentials_exception
        token_data = TokenData(username=username, user_id=uuid.UUID(user_id, version=4))
    except JWTError:
        raise credentials_exception

    result = await db_session.execute(
        select(UserModel)
        .options(selectinload(UserModel.grants))
        .where(UserModel.email == token_data.username)
    )
    user = result.scalars().first()

    return user


async def get_new_email_auth_code() -> str:
    """Генерирует рандомный код авторизации вида 123456"""
    return str(random.randint(100000, 999999))
