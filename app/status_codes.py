"""Модуль статус-кодов HTTP"""
from typing import Any

from fastapi import status

PROJECT_NOT_FOUND: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {"description": "Проект с заданным id не существует"}
}
PROJECT_NOT_OWNER: dict[int | str, dict[str, Any]] = {
    status.HTTP_403_FORBIDDEN: {"description": "Вы не владелец проекта"}
}
PROJECT_NO_PERMISSIONS: dict[int | str, dict[str, Any]] = {
    status.HTTP_403_FORBIDDEN: {"description": "Вы не имеете доступа к проекту"}
}
MUSIC_NOT_FOUND: dict[int | str, dict[str, Any]] = {status.HTTP_400_BAD_REQUEST: {"description": "Музыка не найдена"}}
TEXT_NOT_FOUND: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {"description": "Текста с заданным id не существует"}
}
TEXT_NO_PERMISSIONS: dict[int | str, dict[str, Any]] = {
    status.HTTP_403_FORBIDDEN: {"description": "Вы не имеете доступа к тексту"}
}
CANNOT_REMOVE_SINGLE_TEXT: dict[int | str, dict[str, Any]] = {
    status.HTTP_403_FORBIDDEN: {"description": "Нельзя удалить единственный текст из проекта"}
}
MEANING_NOT_FOUND: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {"description": "Не найдено значение слова"}
}
GRANT_CODE_NOT_FOUND: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {"description": "Код доступа к проекту не найден или деактивирован"}
}
USER_NOT_FOUND: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {"description": "Пользователь с заданным id не найден"}
}
NO_ACCESS_TO_USER_INFO: dict[int | str, dict[str, Any]] = {
    status.HTTP_403_FORBIDDEN: {"description": "У вас нет доступа к информации о пользователе"}
}
