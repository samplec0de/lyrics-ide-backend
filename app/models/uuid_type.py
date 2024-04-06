"""UUID тип для SQLAlchemy: для тестов SQLite версия, для прода PostgreSQL"""
import sys

if "pytest" in sys.modules:
    from sqlalchemy import Uuid as UUIDImpl
else:
    from sqlalchemy.dialects.postgresql import UUID as UUIDImpl  # type: ignore


class UUID(UUIDImpl):  # pylint: disable=too-many-ancestors
    """UUID тип для SQLAlchemy: для тестов SQLite версия, для прода PostgreSQL"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
