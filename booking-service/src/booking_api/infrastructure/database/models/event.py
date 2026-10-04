from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Table, Uuid, func

from booking_api.infrastructure.database.models.base import metadata


class EventSaModel:
    pass


events_table = Table(
    "events",
    metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True, default=uuid4),
    Column("name", String(32), nullable=False),
    Column("description", String(), nullable=False),
    Column("created_at", DateTime(), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(), server_default=func.now(), nullable=False),
)
