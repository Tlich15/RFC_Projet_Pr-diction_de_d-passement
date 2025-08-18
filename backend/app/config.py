from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cors_origins: List[str] = [
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:*",
        "http://127.0.0.1:*",
    ]

    # Point to backend/data
    data_dir: Path = Path(__file__).resolve().parents[1] / "data"

    class Config:
        env_prefix = "APP_"
        case_sensitive = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    return settings