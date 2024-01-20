"""ORM модели"""
from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .user import UserModel  # isort:skip
from .email_auth_code import EmailAuthCodeModel  # isort:skip
from .project import ProjectModel  # isort:skip
