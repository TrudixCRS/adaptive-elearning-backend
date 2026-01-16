from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:HprDPYeVmpisBfJHbxnRXtHxEXkTflqz@postgres.railway.internal:5432/railway"
    JWT_SECRET: str = "1234567890abcdef"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_MINUTES: int = 60 * 24

settings = Settings()
