from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    secret_key: str = "change-me"
    database_url: str = "sqlite:///./pocketsmart.db"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    access_token_expire_minutes: int = 60
    max_upload_mb: int = 5
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    @property
    def upload_dir(self):
        p=Path("uploads"); p.mkdir(parents=True, exist_ok=True); return p

@lru_cache
def get_settings(): return Settings()
