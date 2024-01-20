import random
from typing import Annotated, cast

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
import datetime
from jose import JWTError, jwt
from sqlalchemy import select, ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    email: EmailStr


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception


def get_user(username: str):
    return User(email="user@example.com") if username == "user@example.com" else None


async def create_user_if_not_exists(email: str, db_session: AsyncSession):
    """Добавляет пользователя в базу данных если его там нет"""
    user_query = select(UserModel).where(
        cast(ColumnElement[bool], UserModel.email == email)
    )
    last_code_result = await db_session.execute(user_query)
    if last_code_result.one_or_none() is None:
        user = UserModel(email=email)
        db_session.add(user)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or not isinstance(username, str):
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_new_email_auth_code() -> str:
    """Генерирует рандомный код авторизации вида 123456"""
    return str(random.randint(100000, 999999))
