from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # reads from Railway environment variables, and also from a local .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str

    JWT_SECRET: str = "change-me-in-railway"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_MINUTES: int = 60 * 24  # 1 day


settings = Settings()
