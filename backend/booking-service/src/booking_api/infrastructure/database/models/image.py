from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Table, Uuid, func

from booking_api.infrastructure.database.models.base import metadata


class ImageSaModel:
    pass


images_table = Table(
    "images",
    metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True, default=uuid4),
    Column("url", String(32), nullable=False),
    Column("event_id", Uuid(as_uuid=True), ForeignKey("events.id"), nullable=False),
    Column("created_at", DateTime(), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(), server_default=func.now(), nullable=False),
)
