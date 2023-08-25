from functools import lru_cache
from os import path
from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache(maxsize=None)
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(path.dirname(path.dirname(__file__))).parent / ".env",
        env_file_encoding="utf-8",
    )

    postgres_url: PostgresDsn

    api_id: int
    api_hash: str
