"""ORM модель кода аутентификации по электронной почте"""
import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.models import Base


class EmailAuthCode(Base):  # type: ignore
    """ORM модель кода аутентификации по электронной почте"""

    __tablename__ = "email_auth_code"

    auth_code_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, index=True, unique=True)
    auth_code = Column(String)
