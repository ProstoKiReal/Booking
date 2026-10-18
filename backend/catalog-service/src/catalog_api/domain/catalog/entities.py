from dataclasses import dataclass, field

from catalog_api.domain.catalog.errors import (
    CategoryAlreadyExistsError,
    CategoryNameEmptyError,
    CategoryNameTooLongError,
    CategoryNameTooShortError,
    CategoryOldNameEquivalentNewNameError,
    ImageGalleryInvalidOrderError,
    ImageGalleryInvalidCountError
)
from catalog_api.domain.catalog.value_objects import EventID, CategoryID, ImageID


@dataclass
class Image:
    id: ImageID
    url: str


@dataclass
class GalleryImage:
    image: Image
    order: int

    def __post_init__(self) -> None:
        if self.order not in range(0, 13):
            raise ImageGalleryInvalidOrderError(self.order)


@dataclass
class Event:
    id: EventID
    name: str
    description: str
    category_id: CategoryID
    gallery_images: list[GalleryImage] = field(default_factory=list)

    def __post_init__(self) -> None:
        images_count = len(self.gallery_images)
        if images_count > 12:
            raise ImageGalleryInvalidCountError(images_count)


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

    def rename(self, current_cat_name: str, updated_cat_name: str) -> None:
        if current_cat_name == updated_cat_name:
            raise CategoryOldNameEquivalentNewNameError(current_cat_name, updated_cat_name)
