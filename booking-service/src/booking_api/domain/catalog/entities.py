from dataclasses import dataclass

from booking_api.domain.catalog.errors import (
    CategoryAlreadyExistsError,
    CategoryNameEmptyError,
    CategoryNameTooLongError,
    CategoryNameTooShortError,
)
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

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        if not self.name:
            raise CategoryNameEmptyError()
        if len(self.name) < 2:
            raise CategoryNameTooShortError()
        if len(self.name) > 32:
            raise CategoryNameTooLongError()

    def is_unique(self, already_exists: bool) -> None:
        if already_exists:
            raise CategoryAlreadyExistsError(self.name)


@dataclass
class Image:
    id: ImageID
    url: str
