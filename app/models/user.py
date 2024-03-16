# pylint: disable=cyclic-import
"""ORM модель пользователя"""
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class UserModel(Base):  # type: ignore
    """ORM модель пользователя"""

    __tablename__ = "user"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)

    grants: Mapped[list["ProjectGrantModel"]] = relationship("ProjectGrantModel", back_populates="user", uselist=True)  # type: ignore
