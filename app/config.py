from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    echo_sql: bool = True
    project_name: str = "Lyrics IDE API"
    debug_logs: bool = False


settings = Settings()  # type: ignore
