# pylint: disable=cyclic-import
"""ORM модель гранта (доступа) пользователя к проекту"""
import datetime
import enum
import uuid

from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class GrantLevel(enum.Enum):
    """Уровень доступа к проекту"""

    OWNER = "OWNER"
    READ_WRITE = "READ_WRITE"
    READ_ONLY = "READ_ONLY"


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

    level: Mapped[GrantLevel] = mapped_column(
        Enum(GrantLevel),
        nullable=True,
        index=False,
    )

    # pylint: disable=not-callable
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), index=False, nullable=False)
    # pylint: enable=not-callable

    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="grants")  # type: ignore
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="grants")  # type: ignore


class ProjectGrantCodeModel(Base):  # type: ignore
    """ORM модель кода активации гранта (доступа) пользователя к проекту"""

    __tablename__ = "project_grant_code"

    grant_code_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project.project_id"),
        primary_key=True,
        nullable=False,
        index=True,
    )

    issuer_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.user_id"),
        primary_key=True,
        nullable=False,
        index=True,
    )

    level: Mapped[GrantLevel] = mapped_column(
        Enum(GrantLevel),
        nullable=True,
        index=False,
    )

    max_activations: Mapped[int]
    current_activations: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
        index=False,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
        index=False,
    )

    # pylint: disable=not-callable
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), index=False, nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        index=False,
        nullable=False,
    )
    # pylint: enable=not-callable

    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="grant_codes")  # type: ignore
