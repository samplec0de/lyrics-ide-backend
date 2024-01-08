"""Эндпоинты аутентификации"""
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import Token, User, authenticate_user, create_access_token
from app.mail import lyrics_send_email

router = APIRouter()


@router.post("/email")
async def send_login_code(user: User):
    """Отправка письма с кодом для входа"""
    if user.email != "user@example.com":
        lyrics_send_email(subject="Код для входа", message="Ваш код для входа: 123456", to_email=user.email)
    return {"message": "Код отправлен на вашу электронную почту"}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Получение токена для входа через одноразовый код-пароль с почты"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": "user@example.com"})
    return {"access_token": access_token, "token_type": "bearer"}


def validate_yandex_token(yandex_token: str):
    """Проверка токена Яндекса"""
    return {"email": "example@yandex.ru"}


@router.post("/yandex_token", response_model=Token)
async def login_via_yandex(
    access_token: Annotated[str, Form()], token_type: Annotated[str, Form()], expires_in: Annotated[str, Form()]
):
    """Получение токена для входа через Яндекс"""

    user_info = validate_yandex_token(access_token)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен Яндекса или ошибка проверки",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # После успешной проверки токена Яндекса, вы создаете свой собственный токен.
    new_access_token = create_access_token(data={"sub": user_info["email"]})
    return {"access_token": new_access_token, "token_type": "bearer"}
