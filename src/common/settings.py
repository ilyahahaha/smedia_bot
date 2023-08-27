from functools import lru_cache
from os import path
from pathlib import Path

from pydantic import PostgresDsn, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache(maxsize=None)
class Settings(BaseSettings):
    base_dir: DirectoryPath = Path(path.dirname(path.dirname(__file__)))

    model_config = SettingsConfigDict(
        env_file=base_dir.parent / ".env",
        env_file_encoding="utf-8",
    )

    postgres_url: PostgresDsn

    api_id: int
    api_hash: str
    session_string: str
