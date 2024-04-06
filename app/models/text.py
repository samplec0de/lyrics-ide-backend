# pylint: disable=cyclic-import, unsubscriptable-object
"""ORM модель варианта текста"""
import datetime
import uuid

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base
from app.models.uuid_type import UUID


class TextModel(Base):  # type: ignore
    """ORM модель проекта"""

    __tablename__ = "text"

    text_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project.project_id"),
        nullable=True,
        index=True,
    )
    name: Mapped[str | None]
    # pylint: disable=not-callable
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), index=False, nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        index=False,
        nullable=False,
    )
    # pylint: enable=not-callable

    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="texts")  # type: ignore
