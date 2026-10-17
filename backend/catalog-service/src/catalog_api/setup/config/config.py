from catalog_api.setup.config.db import DBConfig
from catalog_api.setup.config.s3 import S3Config


class Config:
    db: DBConfig = DBConfig()
    s3: S3Config = S3Config()


config = Config()
