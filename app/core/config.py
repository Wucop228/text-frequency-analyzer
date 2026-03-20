import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/word_freq"
    DATABASE_URL_SYNC: str = "postgresql://postgres:postgres@localhost:5432/word_freq"

    UPLOAD_DIR: str = os.path.join(".", "storage", "uploads")
    RESULT_DIR: str = os.path.join(".", "storage", "results")

    MAX_CONCURRENT_TASKS: int = 3

    FILE_READ_CHUNK_SIZE: int = 8 * 1024 * 1024  # 8 MB

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env"),
        extra="ignore"
    )

    def setup_dirs(self):
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.RESULT_DIR, exist_ok=True)


settings = Settings()