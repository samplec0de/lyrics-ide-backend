# pylint: disable=cyclic-import
"""ORM модель кода аутентификации по электронной почте"""
import uuid
from datetime import datetime, timedelta

from sqlalchemy import TIMESTAMP, Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.models import Base


class EmailAuthCodeModel(Base):  # type: ignore
    """ORM модель кода аутентификации по электронной почте"""

    __tablename__ = "email_auth_code"

    auth_code_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, index=True, unique=False)
    auth_code = Column(String)
    valid_to = Column(TIMESTAMP, nullable=False, default=lambda: datetime.now() + timedelta(minutes=15))
    activated_at = Column(TIMESTAMP, nullable=True)
