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
            {"role": "system", "content": settings.openai_prompt},
            {"role": "user", "content": text_input}
        ],
        temperature=settings.openai_temperature,
        max_tokens=150
    )

    return [
        choice.message.content
        for choice in response.choices
    ]
