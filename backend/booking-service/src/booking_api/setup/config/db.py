from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class DBConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="BOOKING_DB_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    NAME: str

    @property
    def URL(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"
