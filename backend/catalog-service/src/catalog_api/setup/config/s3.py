from pydantic_settings import BaseSettings, SettingsConfigDict


class S3Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="S3_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ACCESS_KEY: str
    SECRET_KEY: str
    IMAGES_BUCKET: str
    ENDPOINT_URL: str
    PUBLIC_URL: str
    REGION: str
    SIGNATURE_VERSION: str
    ADDRESSING_STYLE: str
