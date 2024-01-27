# pylint: disable=cyclic-import
"""ORM модель музыки"""
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base, ProjectModel


class MusicModel(Base):  # type: ignore
    """ORM модель музыки"""

    __tablename__ = "music"

    music_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project.project_id"),
        nullable=True,
        index=True,
    )
    url: Mapped[str]
    duration_seconds: Mapped[float]
    bpm: Mapped[int | None]
    custom_bpm: Mapped[int | None]

    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="music")
