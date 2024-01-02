from fastapi import status

PROJECT_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "Проект с заданным id не существует"}}
TEXT_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "Текста с заданным id не существует"}}
MEANING_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "Не найдено значение слова"}}
