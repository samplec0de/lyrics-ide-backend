import datetime
import uuid


class Text:
    """Текст"""
    def __init__(
            self,
            text_id: uuid.UUID,
            project_id: uuid.UUID,
            created_at: datetime.datetime,
            updated_at: datetime.datetime,
    ):
        self.text_id = text_id
        self.project_id = project_id
        self.created_at = created_at
        self.updated_at = updated_at
