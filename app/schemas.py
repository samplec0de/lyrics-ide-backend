from pydantic import BaseModel


class Text(BaseModel):
    name: str = None
    text: str


class Music(BaseModel):
    url: str
    beats_per_minute: int = None


class Project(BaseModel):
    name: str
    description: str = None
    texts: list[Text] = []
    music: Music = None
