from booking_api.setup.config.db import DBConfig


class Config:
    db: DBConfig = DBConfig()


config = Config()
