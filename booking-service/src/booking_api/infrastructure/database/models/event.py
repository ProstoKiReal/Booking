from uuid import uuid4

from sqlalchemy import DateTime, String, Table, Column, ForeignKey, func

from booking_api.infrastructure.database.models.base import metadata


class EventSaModel:
    pass


events_table = Table(
    "events",
    metadata,
    Column("id", primary_key=True, default=uuid4),
    Column("name", String(32), nullable=False),
    Column("description", String(), nullable=False),
    Column("created_at", DateTime(), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(), server_default=func.now(), nullable=False),
)
