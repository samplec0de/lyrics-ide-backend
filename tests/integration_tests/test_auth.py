import pytest
from httpx import AsyncClient

from app.auth import get_new_email_auth_code
from app.models import EmailAuthCodeModel
from tests.conftest import DBSession, client

MAIN_EMAIL = "test@lyrix.xyz"


@pytest.mark.asyncio
async def test_login_for_access_token(db_session: DBSession, client: AsyncClient):
    """Проверка работы аутентификации"""
    new_code = await get_new_email_auth_code()
    new_code_model = EmailAuthCodeModel(email=MAIN_EMAIL, auth_code=new_code)
    db_session.add(new_code_model)
    await db_session.commit()

    response = await client.post(
        "/auth/token",
        data={"username": MAIN_EMAIL, "password": new_code},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]
