"""ORM модели"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для всех ORM моделей"""


from .user import UserModel  # isort:skip
from .email_auth_code import EmailAuthCodeModel  # isort:skip
from .project import ProjectModel  # isort:skip
