from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    echo_sql: bool = True
    project_name: str = "Lyrics IDE API"
    debug_logs: bool = False

    # Секретный ключ для аутентификации по email
    secret_key: str


settings = Settings()  # type: ignore
