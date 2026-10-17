from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from catalog_api.application.dtos.event import (
    CreateEventRequestDTO,
    EventResponseDTO,
    UpdateEventRequestDTO,
)
from catalog_api.application.interfaces.repositories import (
    CategoryRepo,
    EventRepo,
    ImageRepo,
    ImageStorageRepo,
)
from catalog_api.application.interfaces.services import ImageCleanup
from catalog_api.application.mappers import EventMapper
from catalog_api.domain.catalog.errors import (
    CategoryNotFoundError,
    EventNotFoundError,
    ImageNotFoundError,
)
from catalog_api.errors import BaseError
from catalog_api.domain.catalog.value_objects import EventID, ImageID


class CreateEventCommandHandler:
    def __init__(
        self,
        event_repo: EventRepo,
        category_repo: CategoryRepo,
        image_storage_repo: ImageStorageRepo,
        image_cleanup: ImageCleanup,
        session: AsyncSession,
        mapper: EventMapper,
    ) -> None:
        self.event_repo = event_repo
        self.category_repo = category_repo
        self.image_cleanup = image_cleanup
        self.image_storage_repo = image_storage_repo
        self.session = session
        self.mapper = mapper

    async def __call__(
        self,
        event_data: CreateEventRequestDTO,
    ) -> EventResponseDTO:
        uploaded_image_urls: list[str] = []
        try:
            async with self.session.begin():
                category_id = self.mapper.to_category_id(event_data.category_id)
                category = await self.category_repo.get(category_id)
                if category is None:
                    raise CategoryNotFoundError(event_data.category_id)

                uploaded_image_urls = await self.image_storage_repo.save_batch(
                    event_data.images_data
                )
                event = self.mapper.to_create_domain(event_data, uploaded_image_urls)
                created_event = await self.event_repo.create(event)
        except (BaseError, SQLAlchemyError):
            await self.image_cleanup.cleanup_uploaded_images(uploaded_image_urls)
            raise

        return self.mapper.to_dto(created_event)


class UpdateEventCommandHandler:
    def __init__(
        self,
        event_repo: EventRepo,
        image_repo: ImageRepo,
        image_storage_repo: ImageStorageRepo,
        image_cleanup: ImageCleanup,
        session: AsyncSession,
        mapper: EventMapper,
    ) -> None:
        self.event_repo = event_repo
        self.image_repo = image_repo
        self.image_cleanup = image_cleanup
        self.image_storage_repo = image_storage_repo
        self.session = session
        self.mapper = mapper

    async def __call__(
        self,
        event_id: UUID,
        event_data: UpdateEventRequestDTO,
    ) -> EventResponseDTO:
        event_id_value = EventID(event_id)
        uploaded_image_urls: list[str] = []
        try:
            async with self.session.begin():
                event = await self.event_repo.get(event_id_value)
                if event is None:
                    raise EventNotFoundError(event_id)

                for image_data in event_data.images_data:
                    image_id = ImageID(image_data.id)
                    if await self.image_repo.get(image_id) is None:
                        raise ImageNotFoundError(image_data.id)

                uploaded_image_urls = await self.image_storage_repo.save_batch(
                    [image_data.image_data for image_data in event_data.images_data]
                )
                gallery_images = self.mapper.to_updated_gallery_images(
                    event_data.images_data,
                    uploaded_image_urls,
                )
                for gallery_image in gallery_images:
                    updated_image = await self.image_repo.update(
                        gallery_image.image.id,
                        gallery_image.image,
                    )
                    if updated_image is None:
                        raise ImageNotFoundError(gallery_image.image.id.value)
                    gallery_image.image = updated_image

                updated_event_data = self.mapper.to_update_domain(
                    event_id_value,
                    event.category_id,
                    event_data,
                    gallery_images,
                )
                updated_event = await self.event_repo.update(
                    event_id_value,
                    updated_event_data,
                )
                if updated_event is None:
                    raise EventNotFoundError(event_id)
        except (BaseError, SQLAlchemyError):
            await self.image_cleanup.cleanup_uploaded_images(uploaded_image_urls)
            raise

        return self.mapper.to_dto(updated_event)


class DeleteEventCommandHandler:
    def __init__(
        self,
        event_repo: EventRepo,
        session: AsyncSession,
    ) -> None:
        self.event_repo = event_repo
        self.session = session

    async def __call__(self, event_id: UUID) -> None:
        event_id_value = EventID(event_id)
        async with self.session.begin():
            event = await self.event_repo.get(event_id_value)
            if event is None:
                raise EventNotFoundError(event_id)
            await self.event_repo.delete(event_id_value)
