from uuid import uuid4

from sqlalchemy import Column, DateTime, Table, Text, Uuid, func

from catalog_api.infrastructure.database.models.base import metadata


class ImageSaModel:
    pass


images_table = Table(
    "images",
    metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True, default=uuid4),
    Column("url", Text(), nullable=False),
    Column("created_at", DateTime(), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(), server_default=func.now(), nullable=False),
)
