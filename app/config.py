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


settings = Settings()  # type: ignore
