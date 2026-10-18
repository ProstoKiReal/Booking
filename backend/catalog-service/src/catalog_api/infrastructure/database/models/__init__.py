from sqlalchemy.orm import relationship

from catalog_api.infrastructure.database.models.base import mapper_registry
from catalog_api.infrastructure.database.models.category import (
    CategorySaModel,
    categories_table,
)
from catalog_api.infrastructure.database.models.event import EventSaModel, events_table
from catalog_api.infrastructure.database.models.gallery_image import (
    GalleryImageSaModel,
    gallery_images_table,
)
from catalog_api.infrastructure.database.models.image import ImageSaModel, images_table


mapper_registry.map_imperatively(
    EventSaModel,
    events_table,
    properties={
        "category": relationship(CategorySaModel, back_populates="events"),
        "gallery_images": relationship(
            GalleryImageSaModel,
            back_populates="event",
            cascade="all, delete-orphan",
            order_by=(
                gallery_images_table.c.order,
                gallery_images_table.c.image_id,
            ),
        ),
    },
)
mapper_registry.map_imperatively(
    CategorySaModel,
    categories_table,
    properties={"events": relationship(EventSaModel, back_populates="category")},
)
mapper_registry.map_imperatively(
    ImageSaModel,
    images_table,
    properties={
        "gallery_images": relationship(
            GalleryImageSaModel,
            back_populates="image",
            cascade="all, delete-orphan",
        )
    },
)
mapper_registry.map_imperatively(
    GalleryImageSaModel,
    gallery_images_table,
    properties={
        "event": relationship(EventSaModel, back_populates="gallery_images"),
        "image": relationship(ImageSaModel, back_populates="gallery_images"),
    },
)


__all__ = [
    "CategorySaModel",
    "EventSaModel",
    "GalleryImageSaModel",
    "ImageSaModel",
    "mapper_registry",
]
