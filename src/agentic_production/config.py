from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    gemini_api_key: str = ""
    model_name: str = "gemini-2.5-flash"
    environment: str = "development"
    log_level: str = "INFO"
    request_timeout_seconds: float = 30.0
    max_output_tokens: int = 1024
    max_agent_steps: int = 6
    max_tool_calls: int = 8
    default_rate_limit_per_minute: int = 60
    auth_mode: str = "dev"
    dev_bearer_token: str = "dev-token"


@lru_cache
def get_settings() -> Settings:
    return Settings()
