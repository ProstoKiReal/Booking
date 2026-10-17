from catalog_api.application.interfaces.repositories import ImageStorageRepo
from catalog_api.application.interfaces.services import ImageCleanup
from catalog_api.infrastructure.errors import (
    ImageStorageCleanupError,
    ImageStorageError,
)


class ImageCleanupService(ImageCleanup):
    def __init__(self, image_storage_repo: ImageStorageRepo) -> None:
        self.image_storage_repo = image_storage_repo

    async def cleanup_uploaded_images(self, image_urls: list[str]) -> None:
        if not image_urls:
            return
        try:
            await self.image_storage_repo.delete_batch(image_urls)
        except ImageStorageError as error:
            raise ImageStorageCleanupError(
                "Failed to clean up uploaded images."
            ) from error
