from dataclasses import dataclass

from booking_api.domain.catalog.value_objects import EventID, CategoryID, ImageID


@dataclass
class Event:
    id: EventID
    name: str
    description: str
    category_id: CategoryID
    image_id: ImageID


@dataclass
class Category:
    id: CategoryID
    name: str


@dataclass
class Image:
    id: ImageID
    url: str
