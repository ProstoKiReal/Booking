from catalog_api.application.dtos.event import (
    CreateEventRequestDTO,
    EventResponseDTO,
    GetListEventResponseDTO,
    UpdateEventImageDTO,
    UpdateEventRequestDTO,
)
from catalog_api.presentation.http.v1.schemas.event import (
    CreateEventForm,
    EventImageResponse,
    EventResponse,
    GetListEventResponse,
    UpdateEventForm,
)


class EventMapper:
    async def to_create_dto(
        self,
        event_data: CreateEventForm,
    ) -> CreateEventRequestDTO:
        return CreateEventRequestDTO(
            category_id=event_data.category_id,
            name=event_data.name,
            description=event_data.description,
            images_data=[await image.read() for image in event_data.images],
        )

    async def to_update_dto(
        self,
        event_data: UpdateEventForm,
    ) -> UpdateEventRequestDTO:
        return UpdateEventRequestDTO(
            name=event_data.name,
            description=event_data.description,
            images_data=[
                UpdateEventImageDTO(
                    id=image_id,
                    image_data=await image.read(),
                    order=order,
                )
                for image_id, image, order in zip(
                    event_data.image_ids,
                    event_data.images,
                    event_data.orders,
                    strict=True,
                )
            ],
        )

    @staticmethod
    def to_response(event: EventResponseDTO) -> EventResponse:
        return EventResponse(
            id=event.id,
            category_id=event.category_id,
            name=event.name,
            description=event.description,
            images=[
                EventImageResponse(
                    uuid=image.uuid,
                    url=image.url,
                    order=image.order,
                )
                for image in event.images
            ],
        )

    @classmethod
    def to_list_response(
        cls,
        events: GetListEventResponseDTO,
    ) -> GetListEventResponse:
        return GetListEventResponse(
            result=[cls.to_response(event) for event in events.result]
        )
