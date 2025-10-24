from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DB: str = ''
    POSTGRES_USER: str = ''
    POSTGRES_PASSWORD: str = ''
    POSTGRES_SERVER: str = ''
    POSTGRES_PORT: str = ''
    DATABASE_URL: PostgresDsn = ''

    SECRET_KEY: str = ''

    GITHUB_CLIENT_ID: str = ''
    GITHUB_CLIENT_SECRET: str = ''
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
