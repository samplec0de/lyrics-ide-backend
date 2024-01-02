from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status
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
