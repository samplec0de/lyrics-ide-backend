# pylint: disable=cyclic-import
"""ORM модель проекта"""
import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.models import Base


class ProjectModel(Base):  # type: ignore
    """ORM модель проекта"""

    __tablename__ = "project"

    project_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  # type: ignore
    name: str | None = Column(String)  # type: ignore
    description: str | None = Column(String)  # type: ignore
