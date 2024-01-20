# pylint: disable=cyclic-import
"""ORM модель проекта"""
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class ProjectModel(Base):  # type: ignore
    """ORM модель проекта"""

    __tablename__ = "project"

    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str | None]
    description: Mapped[str | None]
