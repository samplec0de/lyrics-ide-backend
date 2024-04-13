"""Функции для интеграции с LLM"""
import json
from typing import cast

from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.openai_api_key)


def get_llm_lyrics_completions(text_input: str):
    """
    Функция принимает на вход часть текста песни и возвращает продолжение этого текста.

    :param text_input: текст для дополнения
    :return: продолжение текста
    """
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": settings.openai_lyrics_prompt},
            {"role": "user", "content": text_input},
        ],
        temperature=settings.openai_temperature,
        max_tokens=150,
        n=settings.openai_lyrics_completions_count,
    )

    return [choice.message.content for choice in response.choices]


def get_llm_rhymes(word: str) -> list[str]:
    """
    Поиск рифмы к слову

    :param word: слово к которому надо подобрать рифму
    :return: рифма
    """
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "system", "content": settings.openai_rhyme_prompt}, {"role": "user", "content": word}],
        response_format={"type": "json_object"},
        temperature=settings.openai_temperature,
        max_tokens=40,
    )

    rhymes = []
    if response.choices:
        try:
            rhymes = json.loads(str(response.choices[0].message.content))["rhymes"]
        except json.JSONDecodeError:
            rhymes = []

    return cast(list[str], rhymes)
