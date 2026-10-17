from abc import abstractmethod
from typing import Protocol


class ImageCleanup(Protocol):
    @abstractmethod
    async def cleanup_uploaded_images(self, image_urls: list[str]) -> None: ...
