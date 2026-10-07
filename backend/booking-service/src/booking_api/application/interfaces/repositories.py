from typing import Protocol
from abc import abstractmethod

from booking_api.domain.catalog.entities import Event, Category, Image
from booking_api.domain.catalog.value_objects import EventID, CategoryID, ImageID


class EventRepo(Protocol):
    @abstractmethod
    async def create(self, event_data: Event) -> Event: ...

    @abstractmethod
    async def get(self, event_id: EventID) -> Event: ...

    @abstractmethod
    async def get_all(self) -> list[Event]: ...

    @abstractmethod
    async def delete(self, event_id: EventID) -> None: ...

    @abstractmethod
    async def update(self, event_id: EventID) -> Event: ...


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
    async def create(self, image_data: Image) ->  Image: ...

    @abstractmethod
    async def delete(self, image_id: ImageID) -> None: ...


class ImageStorageRepo(Protocol):
    @abstractmethod
    async def save(self, image_data: bytes) -> str: ...

    @abstractmethod
    async def delete(self, image_url: str) -> None: ...

    @abstractmethod
    async def get(self, image_url: str) -> bytes: ...
