from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Form, status
from dishka.integrations.fastapi import FromDishka

from catalog_api.application.handlers.commands.events_command_handlers import (
    CreateEventCommandHandler,
    UpdateEventCommandHandler,
    DeleteEventCommandHandler,
)
from catalog_api.domain.catalog.errors import (
    CategoryNotFoundError,
    EventNotFoundError,
    ImageGalleryInvalidCountError,
    ImageGalleryInvalidOrderError,
    ImageNotFoundError,
)
from catalog_api.presentation.http.http_route import DishkaRoute
from catalog_api.presentation.http.v1.mappers.event import EventMapper
from catalog_api.presentation.http.v1.schemas.event import (
    CreateEventForm,
    UpdateEventForm,
    EventResponse,
)

error_map = {
    CategoryNotFoundError: status.HTTP_404_NOT_FOUND,
    EventNotFoundError: status.HTTP_404_NOT_FOUND,
    ImageNotFoundError: status.HTTP_404_NOT_FOUND,
    ImageGalleryInvalidCountError: status.HTTP_400_BAD_REQUEST,
    ImageGalleryInvalidOrderError: status.HTTP_400_BAD_REQUEST,
}


router = APIRouter(
    prefix="/events", 
    tags=["Admin Events"],
    route_class=DishkaRoute,
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=EventResponse,
    error_map=error_map,
)
async def create_event(
    event_data: Annotated[CreateEventForm, Form()],
    handler: FromDishka[CreateEventCommandHandler],
    mapper: FromDishka[EventMapper],
) -> EventResponse:
    request_data = await mapper.to_create_dto(event_data)
    event = await handler(request_data)
    return mapper.to_response(event)


@router.patch(
    "/{event_id}",
    response_model=EventResponse,
    error_map=error_map,
)
async def update_event(
    event_id: UUID,
    event_data: Annotated[UpdateEventForm, Form()],
    handler: FromDishka[UpdateEventCommandHandler],
    mapper: FromDishka[EventMapper],
) -> EventResponse:
    request_data = await mapper.to_update_dto(event_data)
    event = await handler(event_id, request_data)
    return mapper.to_response(event)


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    error_map=error_map,
)
async def delete_event(
    event_id: UUID,
    handler: FromDishka[DeleteEventCommandHandler],
) -> None:
    await handler(event_id)
