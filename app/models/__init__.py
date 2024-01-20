"""ORM модели"""
from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .user import User  # isort:skip
from .email_auth_code import EmailAuthCode  # isort:skip
