from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Required in Railway (set as env var)
    DATABASE_URL: str
    JWT_SECRET: str

    # Optional defaults
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_MINUTES: int = 60 * 24  # 24h

    # allow local .env usage
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
