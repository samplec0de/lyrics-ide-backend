from pydantic import BaseModel, UUID4


class Text(BaseModel):
    name: str = None
    text: str


class Music(BaseModel):
    url: str
    beats_per_minute: int = None


class BaseProject(BaseModel):
    name: str = None
    description: str = None
    texts: list[Text] = []
    music: Music = None


class ProjectIn(BaseProject):
    pass


class ProjectOut(BaseProject):
    id: UUID4
