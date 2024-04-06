# pylint: disable=cyclic-import, unsubscriptable-object
"""ORM модель кода аутентификации по электронной почте"""
import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base
from app.models.uuid_type import UUID


class EmailAuthCodeModel(Base):  # type: ignore
    """ORM модель кода аутентификации по электронной почте"""

    __tablename__ = "email_auth_code"

    auth_code_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    email: Mapped[str] = mapped_column(index=True)
    auth_code: Mapped[str]
    valid_to: Mapped[datetime] = mapped_column(default=lambda: datetime.now() + timedelta(minutes=15))
    activated_at: Mapped[datetime | None]
