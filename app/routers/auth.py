from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status, Path, Form
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import User, create_access_token, Token, authenticate_user

router = APIRouter()


@router.post("/email")
async def send_login_code(user: User):
    if user.email == "user@example.com":
        return {"message": "Login code sent (not really, but pretend)."}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not implemented yet: используй user@example.com")


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
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
    return {"email": "example@yandex.ru"}


@router.post("/yandex_token", response_model=Token)
async def login_via_yandex(access_token: Annotated[str, Form()], token_type: Annotated[str, Form()], expires_in: Annotated[str, Form()]):
    # Здесь должна быть логика проверки токена Яндекса. Это может включать в себя:
    # 1. Отправку запроса на сервер Яндекса для проверки подлинности токена.
    # 2. Валидацию полученной информации.
    # Поскольку каждый сервис имеет свои особенности, обратитесь к документации Яндекса для точных деталей.

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
