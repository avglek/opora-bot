import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"),
        extra='ignore'
    )
    BOT_TOKEN: str
    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"
    LOCAL_DB_PATH:str
    PATH_IMG:str

settings = Settings()

database_url = f'sqlite+aiosqlite:///{settings.LOCAL_DB_PATH}'


