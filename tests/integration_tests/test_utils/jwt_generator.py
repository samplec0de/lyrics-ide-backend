from app.auth import create_user_if_not_exists, create_access_token
from app.config import settings


JWT_SECRET_KEY = settings.secret_key
JWT_ALGORITHM = "HS256"


async def get_jwt_token(email: str, db_session) -> str:
    """
    Генерирует JWT токен для тестирования, регистрируя пользователя, если необходимо.

    :param email: Email пользователя.
    :param db_session: Сессия базы данных для регистрации пользователя.
    :return: JWT токен.
    """
    user = await create_user_if_not_exists(email, db_session)
    access_token = create_access_token(data={"sub": email, "user_id": str(user.user_id)})
    return access_token
