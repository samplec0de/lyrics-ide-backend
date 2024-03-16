# pylint: disable=cyclic-import
"""ORM модель проекта"""
import datetime
import uuid

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class ProjectModel(Base):  # type: ignore
    """ORM модель проекта"""

    __tablename__ = "project"

    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str | None]
    description: Mapped[str | None]
    # pylint: disable=not-callable
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), index=False, nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        index=False,
        nullable=False,
    )
    # pylint: enable=not-callable

    music: Mapped["MusicModel"] = relationship("MusicModel", back_populates="project", uselist=False)  # type: ignore
    texts: Mapped[list["TextModel"]] = relationship("TextModel", back_populates="project", uselist=True)  # type: ignore
    grants: Mapped[list["ProjectGrantModel"]] = relationship("ProjectGrantModel", back_populates="project", uselist=True)  # type: ignore
