from dishka import Provider, Scope, provide

from catalog_api.application.interfaces.repositories import ImageStorageRepo
from catalog_api.application.interfaces.services import ImageCleanup
from catalog_api.infrastructure.storage.image_cleanup import ImageCleanupService


class ServicesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def image_cleanup(self, image_storage_repo: ImageStorageRepo) -> ImageCleanup:
        return ImageCleanupService(image_storage_repo)
