
from typing import TypedDict
from uuid import UUID

from sqlalchemy import Select, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from catalog_api.application.dtos.list_filters import ListFiltersDTO
from catalog_api.application.interfaces.repositories import EventRepo
from catalog_api.domain.catalog.entities import Event, GalleryImage, Image
from catalog_api.domain.catalog.value_objects import CategoryID, EventID, ImageID
from catalog_api.infrastructure.database.models import (
    EventSaModel,
    GalleryImageSaModel,
    ImageSaModel,
)
from catalog_api.infrastructure.database.models.gallery_image import (
    gallery_images_table,
)
from catalog_api.infrastructure.database.repositories.image_repo import (
    AlchemyImageRepo,
)


class GalleryImageModelData(TypedDict):
    event_id: UUID
    image_id: UUID
    order: int


class AlchemyEventRepo(EventRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, event_data: Event) -> Event:
        await self._get_or_create_images(event_data.gallery_images)
        event_model = self.to_model(event_data)
        self.session.add(event_model)
        await self.session.flush()
        gallery_rows = self.to_gallery_images_model_data(
            event_data.id,
            event_data.gallery_images,
        )
        if gallery_rows:
            await self.session.execute(insert(gallery_images_table), gallery_rows)
        await self.session.flush()
        result = await self.session.execute(
            self._get_query().where(EventSaModel.id == event_data.id.value)
        )
        return self.to_domain(result.scalar_one())

    async def get(self, event_id: EventID) -> Event | None:
        result = await self.session.execute(
            self._get_query().where(EventSaModel.id == event_id.value)
        )
        event = result.scalar_one_or_none()
        return self.to_domain(event) if event else None

    async def get_all(self, filters: ListFiltersDTO) -> list[Event]:
        query = self._get_query()
        if filters.category_id is not None:
            query = query.where(
                EventSaModel.category_id == filters.category_id
            )
        result = await self.session.execute(
            query.order_by(EventSaModel.id)
            .offset(filters.offset)
            .limit(filters.limit)
        )
        return [self.to_domain(event) for event in result.scalars().all()]

    async def delete(self, event_id: EventID) -> None:
        event = await self.session.get(EventSaModel, event_id.value)
        if event is not None:
            await self.session.delete(event)
            await self.session.flush()

    async def update(
        self,
        event_id: EventID,
        event_data: Event,
    ) -> Event | None:
        result = await self.session.execute(
            self._get_query().where(EventSaModel.id == event_id.value)
        )
        event_model = result.scalar_one_or_none()
        if event_model is None:
            return None

        await self._get_or_create_images(event_data.gallery_images)
        self.update_model(event_model, event_data)
        await self.session.flush()

        for gallery_image_model in event_model.gallery_images:
            self.session.expunge(gallery_image_model)
        self.session.expire(event_model, ["gallery_images"])
        await self.session.execute(
            delete(gallery_images_table)
            .where(gallery_images_table.c.event_id == event_id.value)
        )
        gallery_rows = self.to_gallery_images_model_data(
            event_id,
            event_data.gallery_images,
        )
        if gallery_rows:
            await self.session.execute(insert(gallery_images_table), gallery_rows)
        await self.session.flush()

        result = await self.session.execute(
            self._get_query().where(EventSaModel.id == event_id.value)
        )
        return self.to_domain(result.scalar_one())

    async def _get_or_create_images(
        self,
        gallery_images: list[GalleryImage],
    ) -> dict[UUID, ImageSaModel]:
        image_ids = {
            gallery_image.image.id.value for gallery_image in gallery_images
        }
        if not image_ids:
            return {}

        result = await self.session.execute(
            select(ImageSaModel).where(ImageSaModel.id.in_(image_ids))
        )
        image_models = {image.id: image for image in result.scalars().all()}

        for gallery_image in gallery_images:
            image_id = gallery_image.image.id.value
            if image_id not in image_models:
                image_model = AlchemyImageRepo.to_model(gallery_image.image)
                self.session.add(image_model)
                image_models[image_id] = image_model

        return image_models

    @staticmethod
    def _get_query() -> Select[tuple[EventSaModel]]:
        return select(EventSaModel).options(
            selectinload(EventSaModel.gallery_images).selectinload(
                GalleryImageSaModel.image
            )
        ).execution_options(populate_existing=True)

    @staticmethod
    def to_model(event_data: Event) -> EventSaModel:
        return EventSaModel(
            id=event_data.id.value,
            name=event_data.name,
            description=event_data.description,
            category_id=event_data.category_id.value,
        )

    @staticmethod
    def to_gallery_image_model_data(
        event_id: EventID,
        gallery_image_data: GalleryImage,
    ) -> GalleryImageModelData:
        return {
            "event_id": event_id.value,
            "image_id": gallery_image_data.image.id.value,
            "order": gallery_image_data.order,
        }

    @classmethod
    def to_gallery_images_model_data(
        cls,
        event_id: EventID,
        gallery_images_data: list[GalleryImage],
    ) -> list[GalleryImageModelData]:
        return [
            cls.to_gallery_image_model_data(event_id, gallery_image_data)
            for gallery_image_data in gallery_images_data
        ]

    @staticmethod
    def update_model(event_model: EventSaModel, event_data: Event) -> None:
        event_model.name = event_data.name
        event_model.description = event_data.description
        event_model.category_id = event_data.category_id.value

    @staticmethod
    def to_domain(event: EventSaModel) -> Event:
        return Event(
            id=EventID(event.id),
            name=event.name,
            description=event.description,
            category_id=CategoryID(event.category_id),
            gallery_images=[
                GalleryImage(
                    image=Image(
                        id=ImageID(gallery_image.image.id),
                        url=gallery_image.image.url,
                    ),
                    order=gallery_image.order,
                )
                for gallery_image in event.gallery_images
            ],
        )
