from dishka import Provider, Scope

from catalog_api.application.interfaces.repositories import ImageStorageRepo
from catalog_api.application.interfaces.services import ImageCleanup
from catalog_api.infrastructure.storage.image_cleanup import ImageCleanupService


def services_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(source=ImageCleanupService, provides=ImageCleanup)
    return provider
