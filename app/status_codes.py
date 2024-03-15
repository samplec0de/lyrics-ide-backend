from typing import Any

from fastapi import status

PROJECT_NOT_FOUND: dict[int | str, dict[str, Any]] = {status.HTTP_404_NOT_FOUND: {"description": "Проект с заданным id не существует"}}
MUSIC_NOT_FOUND: dict[int | str, dict[str, Any]] = {status.HTTP_400_BAD_REQUEST: {"description": "Музыка не найдена"}}
TEXT_NOT_FOUND: dict[int | str, dict[str, Any]] = {status.HTTP_404_NOT_FOUND: {"description": "Текста с заданным id не существует"}}
CANNOT_REMOVE_SINGLE_TEXT: dict[int | str, dict[str, Any]] = {status.HTTP_403_FORBIDDEN: {"description": "Нельзя удалить единственный текст из проекта"}}
MEANING_NOT_FOUND: dict[int | str, dict[str, Any]] = {status.HTTP_404_NOT_FOUND: {"description": "Не найдено значение слова"}}
