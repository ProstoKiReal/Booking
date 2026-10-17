from abc import abstractmethod
from typing import Protocol

from fastapi import UploadFile

from catalog_api.domain.catalog.entities import Category, Event, GalleryImage, Image
from catalog_api.domain.catalog.value_objects import EventID, CategoryID, ImageID


class EventRepo(Protocol):
    @abstractmethod
    async def create(self, event_data: Event) -> Event: ...

    @abstractmethod
    async def get(self, event_id: EventID) -> Event | None: ...

    @abstractmethod
    async def get_all(self) -> list[Event]: ...

    @abstractmethod
    async def delete(self, event_id: EventID) -> None: ...

    @abstractmethod
    async def update(self, event_id: EventID, event_data: Event) -> Event | None: ...


class CategoryRepo(Protocol):
    @abstractmethod
    async def create(self, category_data: Category) -> Category: ...

    @abstractmethod
    async def exists_by_name(self, name: str) -> bool: ...

    @abstractmethod
    async def get(self, category_id: CategoryID) -> Category | None: ...

    @abstractmethod
    async def get_all(self) -> list[Category]: ...

    @abstractmethod
    async def delete(self, category_id: CategoryID) -> None: ...

    @abstractmethod
    async def update(self, category: Category) -> Category: ...


class ImageRepo(Protocol):
    @abstractmethod
    async def create(self, image_data: Image) -> Image: ...

    @abstractmethod
    async def get(self, image_id: ImageID) -> Image | None: ...

    @abstractmethod
    async def get_all(self) -> list[Image]: ...

    @abstractmethod
    async def update(
        self,
        image_id: ImageID,
        image_data: Image,
    ) -> Image | None: ...

    @abstractmethod
    async def delete(self, image_id: ImageID) -> None: ...


class GalleryImageRepo(Protocol):
    @abstractmethod
    async def create(
        self,
        event_id: EventID,
        gallery_image_data: GalleryImage,
    ) -> GalleryImage: ...

    @abstractmethod
    async def get(
        self,
        event_id: EventID,
        image_id: ImageID,
    ) -> GalleryImage | None: ...

    @abstractmethod
    async def get_all(self, event_id: EventID) -> list[GalleryImage]: ...

    @abstractmethod
    async def update(
        self,
        event_id: EventID,
        image_id: ImageID,
        gallery_image_data: GalleryImage,
    ) -> GalleryImage | None: ...

    @abstractmethod
    async def delete(self, event_id: EventID, image_id: ImageID) -> None: ...


class ImageStorageRepo(Protocol):
    @abstractmethod
    async def save(self, image_data: UploadFile) -> str: ...

    @abstractmethod
    async def save_batch(self, images_data: list[UploadFile]) -> list[str]: ...

    @abstractmethod
    async def delete(self, image_url: str) -> None: ...

    @abstractmethod
    async def delete_batch(self, image_urls: list[str]) -> None: ...

    @abstractmethod
    async def get(self, image_url: str) -> bytes: ...
