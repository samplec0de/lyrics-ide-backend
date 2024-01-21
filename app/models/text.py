# pylint: disable=cyclic-import
"""ORM модель варианта текста"""
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


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
    url: Mapped[str]

    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="texts")  # type: ignore
