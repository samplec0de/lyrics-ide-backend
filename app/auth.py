import random
import uuid
from typing import Annotated, cast

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, UUID4
import datetime
from jose import JWTError, jwt
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
    user_id: str


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
        if username is None or not isinstance(username, str):
            raise credentials_exception
        token_data = TokenData(username=username, user_id=payload.get("user_id"))
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
        if username is None or not isinstance(username, str):
            raise credentials_exception
        token_data = TokenData(username=username, user_id=payload.get("user_id"))
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
