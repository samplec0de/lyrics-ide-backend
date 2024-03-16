from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    echo_sql: bool = True
    project_name: str = "Lyrics IDE API"
    debug_logs: bool = False

    # Секретный ключ для аутентификации по email
    secret_key: str

    # Количество дней, на которое выдается токен
    token_expire_days: int = 30

    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str

    yandex_dict_key: str

    mongo_url: str

    tiptap_app_id: str
    tiptap_secret_key: str

    openai_lyrics_prompt: str = ("Продолжи текст песни. "
                          "В ответ пришли текст, который нужно добавить. учитывай регистр, старайся рифмовать")
    openai_lyrics_completions_count: int = 2
    openai_rhyme_prompt: str = ("Подбери рифму к слову для текста песни. "
                                "В ответ пришли в формате JSON. "
                                "По ключу rhymes массив рифмующихся слов или словосочетаний. "
                                "Пример: {\"rhymes\": [...]}")
    openai_model: str = "gpt-3.5-turbo-0125"
    openai_temperature: float = 0.7
    openai_api_key: str
    openai_max_tokens: int = 150


settings = Settings()  # type: ignore
