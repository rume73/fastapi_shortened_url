import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field, PostgresDsn

logging_config.dictConfig(LOGGING)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHORT_URL_LEN = 8


class AppSettings(BaseSettings):
    app_title: str = 'UrlShortenerApp'
    database_dsn: PostgresDsn = Field(
        'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres',
        env='DATABASE_DSN',
    )
    project_host: str = Field(..., env='PROJECT_HOST')
    project_port: int = Field(8000, env='PROJECT_PORT')
    black_list: list[str] = [
        # '172.22.0.1',
    ]

    class Config:
        env_file = '.env'


app_settings = AppSettings()
