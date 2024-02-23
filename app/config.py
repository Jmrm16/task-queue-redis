from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Queue Redis API"
    API_V1_STR: str = "/api/v1"
    REDIS_URL: str = "redis://localhost:6379/0"
    DEFAULT_MAX_RETRIES: int = 3
    DEFAULT_BACKOFF_FACTOR: float = 1.5

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


settings = Settings()
