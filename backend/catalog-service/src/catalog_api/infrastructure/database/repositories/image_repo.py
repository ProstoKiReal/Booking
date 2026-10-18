from sqlalchemy import case, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from catalog_api.application.interfaces.repositories import ImageRepo
from catalog_api.domain.catalog.entities import Image
from catalog_api.domain.catalog.value_objects import ImageID
from catalog_api.infrastructure.database.models import ImageSaModel


class AlchemyImageRepo(ImageRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, image_data: Image) -> Image:
        image_model = self.to_model(image_data)
        self.session.add(image_model)
        await self.session.flush()
        return self.to_domain(image_model)

    async def get(self, image_id: ImageID) -> Image | None:
        image = await self.session.get(ImageSaModel, image_id.value)
        return self.to_domain(image) if image else None

    async def get_all(self) -> list[Image]:
        result = await self.session.execute(
            select(ImageSaModel).order_by(ImageSaModel.id)
        )
        return [self.to_domain(image) for image in result.scalars().all()]

    async def update(self, image_id: ImageID, image_data: Image) -> Image | None:
        image_model = await self.session.get(ImageSaModel, image_id.value)
        if image_model is None:
            return None

        self.update_model(image_model, image_data)
        await self.session.flush()
        return self.to_domain(image_model)

    async def update_batch(self, images_data: list[Image]) -> list[Image]:
        if not images_data:
            return []

        image_urls = {
            image.id.value: image.url
            for image in images_data
        }
        result = await self.session.execute(
            update(ImageSaModel)
            .where(ImageSaModel.id.in_(image_urls))
            .values(url=case(image_urls, value=ImageSaModel.id))
            .returning(ImageSaModel)
        )
        updated_images = {
            image.id: self.to_domain(image)
            for image in result.scalars().all()
        }
        return [
            updated_images[image.id.value]
            for image in images_data
            if image.id.value in updated_images
        ]

    async def delete(self, image_id: ImageID) -> None:
        image = await self.session.get(ImageSaModel, image_id.value)
        if image is not None:
            await self.session.delete(image)
            await self.session.flush()

    @staticmethod
    def to_domain(image: ImageSaModel) -> Image:
        return Image(id=ImageID(image.id), url=image.url)

    @staticmethod
    def to_model(image_data: Image) -> ImageSaModel:
        return ImageSaModel(
            id=image_data.id.value,
            url=image_data.url,
        )

    @staticmethod
    def update_model(image_model: ImageSaModel, image_data: Image) -> None:
        image_model.url = image_data.url
