from sqlalchemy import Column, ForeignKey, Integer, Table, Uuid

from catalog_api.infrastructure.database.models.base import metadata


class GalleryImageSaModel:
    pass


gallery_images_table = Table(
    "gallery_images",
    metadata,
    Column(
        "event_id",
        Uuid(as_uuid=True),
        ForeignKey("events.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "image_id",
        Uuid(as_uuid=True),
        ForeignKey("images.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("order", Integer(), nullable=False),
)
