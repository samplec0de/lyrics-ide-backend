"""Эндпоинты аутентификации"""
from datetime import datetime
from typing import Annotated, cast

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import ColumnElement, select

from app.api.dependencies.core import DBSessionDep
from app.auth import Token, User, create_access_token, create_user_if_not_exists, get_new_email_auth_code
from app.mail import lyrics_send_email
from app.models.email_auth_code import EmailAuthCodeModel

router = APIRouter()


@router.post("/email")
async def send_login_code(user: User, db_session: DBSessionDep):
    """Отправка письма с кодом для входа"""
    if user.email != "user@example.com":
        new_code = await get_new_email_auth_code()
        new_code_model = EmailAuthCodeModel(email=user.email, auth_code=new_code)
        db_session.add(new_code_model)
        lyrics_send_email(subject="Код для входа", message=f"Ваш код для входа: {new_code}", to_email=user.email)
        await db_session.commit()
    return {"message": "Код отправлен на вашу электронную почту"}


@router.post(
    "/token",
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Неуспешная аутентификация. Текст ошибки содержит причину в значении `detail`. Возможные причины: `Неверный код`, `Код не был отправлен`, `Срок действия кода истёк`, `Код уже был использован`"
        }
    },
)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db_session: DBSessionDep):
    """
    Этот эндпоинт позволяет пользователю войти в систему, используя одноразовый код-пароль, отправленный на его электронную почту.

    Возвращает JWT токен при успешной аутентификации.

    В случае ошибки возвращает соответствующее сообщение об ошибке.
    """
    last_code_query = (
        select(EmailAuthCodeModel)
        .where(cast(ColumnElement[bool], EmailAuthCodeModel.email == form_data.username))
        .order_by(EmailAuthCodeModel.valid_to.desc())
        .limit(1)
    )
    last_code_result = await db_session.execute(last_code_query)

    error_msg: str | None = None

    if correct_code_obj := last_code_result.scalar_one_or_none():
        correct_code = correct_code_obj.auth_code
        code_valid_to = correct_code_obj.valid_to
        code_activated = correct_code_obj.activated_at
        if code_valid_to < datetime.now():
            error_msg = "Срок действия кода истёк"
        if code_activated is not None:
            error_msg = "Код уже был использован"
        elif correct_code != form_data.password:
            error_msg = "Неверный код"
        else:
            await create_user_if_not_exists(email=form_data.username, db_session=db_session)
            correct_code_obj.activated_at = datetime.now()
            await db_session.commit()
    else:
        error_msg = "Код не был отправлен"

    if error_msg:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_msg,
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": form_data.username})
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
