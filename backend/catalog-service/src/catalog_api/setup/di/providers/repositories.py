from dishka import Provider, Scope, provide
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


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def category_repo(self, session: AsyncSession) -> CategoryRepo:
        return AlchemyCategoryRepo(session=session)

    @provide
    def event_repo(self, session: AsyncSession) -> EventRepo:
        return AlchemyEventRepo(session=session)

    @provide
    def gallery_image_repo(self, session: AsyncSession) -> GalleryImageRepo:
        return AlchemyGalleryImageRepo(session=session)

    @provide
    def image_repo(self, session: AsyncSession) -> ImageRepo:
        return AlchemyImageRepo(session=session)

    @provide
    def image_storage_repo(
        self,
        client: AioBaseClient,
        config: Config,
    ) -> ImageStorageRepo:
        return AioBotocoreImageStorageRepo(
            client=client,
            bucket=config.s3.IMAGES_BUCKET,
            public_endpoint=config.s3.PUBLIC_URL,
        )
