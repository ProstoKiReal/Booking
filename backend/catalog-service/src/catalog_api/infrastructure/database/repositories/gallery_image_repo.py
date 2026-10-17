from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from catalog_api.application.interfaces.repositories import GalleryImageRepo
from catalog_api.domain.catalog.entities import GalleryImage, Image
from catalog_api.domain.catalog.value_objects import EventID, ImageID
from catalog_api.infrastructure.database.models import GalleryImageSaModel


class AlchemyGalleryImageRepo(GalleryImageRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        event_id: EventID,
        gallery_image_data: GalleryImage,
    ) -> GalleryImage:
        gallery_image_model = self.to_model(event_id, gallery_image_data)
        self.session.add(gallery_image_model)
        await self.session.flush()
        result = await self.session.execute(
            self._get_query().where(
                GalleryImageSaModel.event_id == event_id.value,
                GalleryImageSaModel.image_id == gallery_image_data.image.id.value,
            )
        )
        return self.to_domain(result.scalar_one())

    async def get(
        self,
        event_id: EventID,
        image_id: ImageID,
    ) -> GalleryImage | None:
        result = await self.session.execute(
            self._get_query().where(
                GalleryImageSaModel.event_id == event_id.value,
                GalleryImageSaModel.image_id == image_id.value,
            )
        )
        gallery_image = result.scalar_one_or_none()
        return self.to_domain(gallery_image) if gallery_image else None

    async def get_all(self, event_id: EventID) -> list[GalleryImage]:
        result = await self.session.execute(
            self._get_query()
            .where(GalleryImageSaModel.event_id == event_id.value)
            .order_by(GalleryImageSaModel.order, GalleryImageSaModel.image_id)
        )
        return [
            self.to_domain(gallery_image)
            for gallery_image in result.scalars().all()
        ]

    async def update(
        self,
        event_id: EventID,
        image_id: ImageID,
        gallery_image_data: GalleryImage,
    ) -> GalleryImage | None:
        result = await self.session.execute(
            self._get_query().where(
                GalleryImageSaModel.event_id == event_id.value,
                GalleryImageSaModel.image_id == image_id.value,
            )
        )
        gallery_image_model = result.scalar_one_or_none()
        if gallery_image_model is None:
            return None

        self.update_model(gallery_image_model, gallery_image_data)
        await self.session.flush()
        return self.to_domain(gallery_image_model)

    async def delete(self, event_id: EventID, image_id: ImageID) -> None:
        gallery_image = await self.session.get(
            GalleryImageSaModel,
            (event_id.value, image_id.value),
        )
        if gallery_image is not None:
            await self.session.delete(gallery_image)
            await self.session.flush()

    @staticmethod
    def _get_query() -> Select[tuple[GalleryImageSaModel]]:
        return select(GalleryImageSaModel).options(
            selectinload(GalleryImageSaModel.image)
        )

    @staticmethod
    def to_domain(gallery_image: GalleryImageSaModel) -> GalleryImage:
        return GalleryImage(
            image=Image(
                id=ImageID(gallery_image.image.id),
                url=gallery_image.image.url,
            ),
            order=gallery_image.order,
        )

    @staticmethod
    def to_model(
        event_id: EventID,
        gallery_image_data: GalleryImage,
    ) -> GalleryImageSaModel:
        return GalleryImageSaModel(
            event_id=event_id.value,
            image_id=gallery_image_data.image.id.value,
            order=gallery_image_data.order,
        )

    @staticmethod
    def update_model(
        gallery_image_model: GalleryImageSaModel,
        gallery_image_data: GalleryImage,
    ) -> None:
        gallery_image_model.order = gallery_image_data.order
