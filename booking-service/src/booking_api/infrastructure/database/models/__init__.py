from sqlalchemy.orm import relationship

from booking_api.infrastructure.database.models.base import mapper_registry
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
        "categories": relationship(CategorySaModel, back_populates="event"),
        "images": relationship(ImageSaModel, back_populates="event"),
    },
)
mapper_registry.map_imperatively(
    CategorySaModel,
    categories_table,
    properties={"event": relationship(EventSaModel, back_populates="categories")},
)
mapper_registry.map_imperatively(
    ImageSaModel,
    images_table,
    properties={"event": relationship(EventSaModel, back_populates="images")},
)


__all__ = [
    "CategorySaModel",
    "EventSaModel",
    "ImageSaModel",
    "mapper_registry",
]
