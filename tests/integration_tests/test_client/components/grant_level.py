import enum


class GrantLevel(enum.Enum):
    """Уровень доступа к проекту"""

    READ_WRITE = "READ_WRITE"
    READ_ONLY = "READ_ONLY"
