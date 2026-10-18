from dishka import Provider, Scope
from aiobotocore.client import AioBaseClient
from sqlalchemy.ext.asyncio import AsyncSession

from catalog_api.application.interfaces.repositories import (
    CategoryRepo,
    EventRepo,
    GalleryImageRepo,
    ImageRepo,
    ImageStorageRepo,
)
from catalog_api.infrastructure.database.repositories.category_repo import AlchemyCategoryRepo
from catalog_api.infrastructure.database.repositories.event_repo import AlchemyEventRepo
from catalog_api.infrastructure.database.repositories.gallery_image_repo import (
    AlchemyGalleryImageRepo,
)
from catalog_api.infrastructure.database.repositories.image_repo import AlchemyImageRepo
from catalog_api.infrastructure.storage.image import AioBotocoreImageStorageRepo
from catalog_api.setup.config import Config


def image_storage_repo(
    client: AioBaseClient,
    config: Config,
) -> ImageStorageRepo:
    return AioBotocoreImageStorageRepo(
        client=client,
        bucket=config.s3.IMAGES_BUCKET,
        public_endpoint=config.s3.PUBLIC_URL,
    )


def repositories_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(source=AlchemyCategoryRepo, provides=CategoryRepo)
    provider.provide(source=AlchemyEventRepo, provides=EventRepo)
    provider.provide(source=AlchemyGalleryImageRepo, provides=GalleryImageRepo)
    provider.provide(source=AlchemyImageRepo, provides=ImageRepo)
    provider.provide(source=image_storage_repo)
    return provider
