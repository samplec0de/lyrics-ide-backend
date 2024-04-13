"""Модуль с исключениями"""


class PermissionDeniedError(Exception):
    """Ошибка доступа"""


class NotFoundError(Exception):
    """Объект не найден"""


class TextNotFoundError(NotFoundError):
    """Текст не найден"""


class ProjectNotFoundError(NotFoundError):
    """Проект не найден"""


class UnAuthorizedError(Exception):
    """Ошибка авторизации"""


class MusicNotFoundError(NotFoundError):
    """Музыка не найдена"""
