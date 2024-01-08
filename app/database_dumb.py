from uuid import UUID

from pydantic import UUID4

from app.api.schemas import ProjectOut, TextVariant, MusicOut

projects: dict[UUID4, ProjectOut] = {
    UUID("82742b97-004e-4746-aed7-c2eaac815e6e"): ProjectOut(
        id=UUID("82742b97-004e-4746-aed7-c2eaac815e6e"),
        name="Проект 1",
        description="Описание проекта 1",
        texts=[
            TextVariant(
                id=UUID("fffb646c-d846-409f-8b2b-e248a611c7b2"),
                name="Вариант текста 1",
                text="Текст 1",
            ),
            TextVariant(
                id=UUID("ad45ff94-9c09-40b2-a50a-eba63848298d"),
                name="Вариант текста 2",
                text="Текст 2",
            ),
        ],
        music=MusicOut(
            url="https://lyrics-ide.storage.yandexcloud.net/beat_stub.mp3",
            duration_seconds=184,
            bpm=90,
        )
    ),
}

project_texts: dict[UUID4, TextVariant] = {
    UUID("fffb646c-d846-409f-8b2b-e248a611c7b2"): TextVariant(
        id=UUID("fffb646c-d846-409f-8b2b-e248a611c7b2"),
        name="Вариант текста 1",
        text="Текст 1",
    ),
    UUID("ad45ff94-9c09-40b2-a50a-eba63848298d"): TextVariant(
        id=UUID("ad45ff94-9c09-40b2-a50a-eba63848298d"),
        name="Вариант текста 2",
        text="Текст 2",
    ),
}
