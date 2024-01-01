from fastapi import UploadFile
from pydantic import BaseModel, UUID4


class Text(BaseModel):
    name: str = None
    text: str


class MusicBase(BaseModel):
    pass


class MusicIn(MusicBase):
    file: UploadFile = None


class MusicOut(MusicBase):
    url: str
    duration_seconds: int
    bpm: int
    custom_bpm: int = None


class ProjectBase(BaseModel):
    name: str = None
    description: str = None
    texts: list[Text] = []
    music: MusicIn = None


class ProjectIn(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: UUID4
    music: MusicOut = None
