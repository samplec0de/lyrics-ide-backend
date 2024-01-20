# pylint: disable=cyclic-import
"""ORM модель пользователя"""
import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.models import Base


class UserModel(Base):  # type: ignore
    """ORM модель пользователя"""

    __tablename__ = "user"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, index=True, unique=True)
