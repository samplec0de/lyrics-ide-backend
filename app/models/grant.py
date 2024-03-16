# pylint: disable=cyclic-import
"""ORM модель гранта (доступа) пользователя к проекту"""
import datetime
import uuid

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class ProjectGrantModel(Base):  # type: ignore
    """ORM модель гранта (доступа) пользователя к проекту"""

    __tablename__ = "project_grant"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project.project_id"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.user_id"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    # pylint: disable=not-callable
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), index=False, nullable=False)
    # pylint: enable=not-callable

    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="grants")  # type: ignore
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="grants")  # type: ignore
