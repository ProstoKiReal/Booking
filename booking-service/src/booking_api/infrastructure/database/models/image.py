from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Table, Column, func

from booking_api.infrastructure.database.models.base import metadata


class ImageSaModel:
    pass


images_table = Table(
    "images",
    metadata,
    Column("id", primary_key=True, default=uuid4),
    Column("url", String(32), nullable=False),
    Column("event_id", ForeignKey("events.id"), nullable=False),
    Column("created_at", DateTime(), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(), server_default=func.now(), nullable=False),
)
