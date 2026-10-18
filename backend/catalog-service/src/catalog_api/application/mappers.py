from uuid import UUID

from catalog_api.application.dtos.category import (
    CategoryName,
    CreateCategoryResponseDTO,
    GetCategoryResponseDTO,
    GetListCategoryResponseDTO,
    UpdateCategoryResponseDTO,
)
from catalog_api.application.dtos.event import (
    CreateEventRequestDTO,
    EventImageResponseDTO,
    EventResponseDTO,
    GetListEventResponseDTO,
    UpdateEventImageDTO,
    UpdateEventRequestDTO,
)
from catalog_api.domain.catalog.entities import Category, Event, GalleryImage, Image
from catalog_api.domain.catalog.value_objects import CategoryID, EventID, ImageID


class CategoryMapper:
    def to_domain(
        self,
        category_data: CategoryName,
        category_id: CategoryID | None = None,
    ) -> Category:
        return Category(
            id=category_id or CategoryID.new(),
            name=category_data.name,
        )

    def to_dto(self, category: Category) -> CreateCategoryResponseDTO:
        return CreateCategoryResponseDTO(
            id=category.id.value,
            name=category.name,
        )

    def to_update_dto(self, category: Category) -> UpdateCategoryResponseDTO:
        return UpdateCategoryResponseDTO(
            id=category.id.value,
            name=category.name,
        )

    def to_get_dto(self, category: Category) -> GetCategoryResponseDTO:
        return GetCategoryResponseDTO(
            id=category.id.value,
            name=category.name,
        )

    def to_list_dto(self, categories: list[Category]) -> GetListCategoryResponseDTO:
        return GetListCategoryResponseDTO(
            result=[self.to_get_dto(category) for category in categories]
        )


class EventMapper:
    @staticmethod
    def to_category_id(category_id: UUID) -> CategoryID:
        return CategoryID(category_id)

    @staticmethod
    def to_create_domain(
        event_data: CreateEventRequestDTO,
        image_urls: list[str],
    ) -> Event:
        return Event(
            id=EventID.new(),
            name=event_data.name,
            description=event_data.description,
            category_id=CategoryID(event_data.category_id),
            gallery_images=[
                GalleryImage(
                    image=Image(id=ImageID.new(), url=image_url),
                    order=order,
                )
                for order, image_url in enumerate(image_urls)
            ],
        )

    @staticmethod
    def to_updated_gallery_images(
        images_data: list[UpdateEventImageDTO],
        image_urls: list[str],
    ) -> list[GalleryImage]:
        return [
            GalleryImage(
                image=Image(id=ImageID(image_data.id), url=image_url),
                order=image_data.order,
            )
            for image_data, image_url in zip(images_data, image_urls, strict=True)
        ]

    @staticmethod
    def to_update_domain(
        event_id: EventID,
        category_id: CategoryID,
        event_data: UpdateEventRequestDTO,
        gallery_images: list[GalleryImage],
    ) -> Event:
        return Event(
            id=event_id,
            name=event_data.name,
            description=event_data.description,
            category_id=category_id,
            gallery_images=gallery_images,
        )

    @staticmethod
    def to_dto(event: Event) -> EventResponseDTO:
        return EventResponseDTO(
            id=event.id.value,
            category_id=event.category_id.value,
            name=event.name,
            description=event.description,
            images=[
                EventImageResponseDTO(
                    uuid=gallery_image.image.id.value,
                    url=gallery_image.image.url,
                    order=gallery_image.order,
                )
                for gallery_image in event.gallery_images
            ],
        )

    @classmethod
    def to_list_dto(cls, events: list[Event]) -> GetListEventResponseDTO:
        return GetListEventResponseDTO(
            result=[cls.to_dto(event) for event in events]
        )
