from dishka import Provider, Scope, provide
from aiobotocore.client import AioBaseClient
from sqlalchemy.ext.asyncio import AsyncSession

from catalog_api.application.interfaces.repositories import (
    CategoryRepo,
    ImageStorageRepo,
)
from catalog_api.infrastructure.database.repositories.category_repo import AlchemyCategoryRepo
from catalog_api.infrastructure.storage.image import AioBotocoreImageStorageRepo
from catalog_api.setup.config import Config


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def category_repo(self, session: AsyncSession) -> CategoryRepo:
        return AlchemyCategoryRepo(session=session)

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
