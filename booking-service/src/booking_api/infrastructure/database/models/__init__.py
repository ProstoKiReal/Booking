from sqlalchemy.orm import relationship

from booking_api.infrastructure.database.models.base import (
    BaseSaModel,
    mapper_registry,
    metadata,
)
from booking_api.infrastructure.database.models.category import (
    CategorySaModel,
    categories_table,
)
from booking_api.infrastructure.database.models.event import EventSaModel, events_table
from booking_api.infrastructure.database.models.image import ImageSaModel, images_table


mapper_registry.map_imperatively(
    EventSaModel,
    events_table,
    properties={
        "category": relationship(CategorySaModel, back_populates="event"),
        "image": relationship(ImageSaModel, back_populates="event"),
    },
)
mapper_registry.map_imperatively(
    CategorySaModel,
    categories_table,
    properties={"event": relationship(EventSaModel, back_populates="category")},
)
mapper_registry.map_imperatively(
    ImageSaModel,
    images_table,
    properties={"event": relationship(EventSaModel, back_populates="image")},
)


__all__ = [
    "BaseSaModel",
    "CategorySaModel",
    "EventSaModel",
    "ImageSaModel",
]
