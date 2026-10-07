from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Table, Uuid, UniqueConstraint, func

from booking_api.infrastructure.database.models.base import metadata


class CategorySaModel:
    pass


categories_table = Table(
    "categiries",
    metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True, default=uuid4),
    Column("name", String(32), nullable=False),
    Column("created_at", DateTime(), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(), server_default=func.now(), nullable=False),
    UniqueConstraint("name", name="uq_categiries_name"),
)
