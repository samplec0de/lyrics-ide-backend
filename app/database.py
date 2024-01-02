from uuid import UUID

from pydantic import UUID4

from app.schemas import ProjectOut, TextVariant

projects: dict[UUID4, ProjectOut] = {
    UUID("82742b97-004e-4746-aed7-c2eaac815e6e"): ProjectOut(
        id="82742b97-004e-4746-aed7-c2eaac815e6e",
        name="Проект 1",
        description="Описание проекта 1",
        texts=[
            TextVariant(
                id="82742b97-004e-4746-aed7-c2eaac815e6e",
                name="Вариант текста 1",
                text="Текст 1",
            ),
            TextVariant(
                id="82742b97-004e-4746-aed7-c2eaac815e6e",
                name="Вариант текста 2",
                text="Текст 2",
            ),
        ],
    ),
}

project_texts: dict[UUID4, TextVariant] = {}
