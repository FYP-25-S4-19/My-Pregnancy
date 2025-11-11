from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int

    @property
    def DATABASE_URL(self) -> str:
        user = self.POSTGRES_USER
        password = self.POSTGRES_PASSWORD
        server = self.POSTGRES_SERVER
        port = self.POSTGRES_PORT
        db = self.POSTGRES_DB
        return f"postgresql+psycopg2://{user}:{password}@{server}:{port}/{db}"

    SECRET_KEY: str

    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str

    APP_ENV: str

    # CONSTANTS
    JWT_EXPIRATION_MINUTES: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
