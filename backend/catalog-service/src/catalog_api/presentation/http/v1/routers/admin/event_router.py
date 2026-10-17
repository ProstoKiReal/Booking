from typing import Annotated
from uuid import UUID

from fastapi import File, Form, HTTPException, UploadFile, status
from dishka.integrations.fastapi import FromDishka
from fastapi_error_map import ErrorAwareRouter
from pydantic import Field, ValidationError

from catalog_api.presentation.http.http_route import DishkaErrorAwareRoute
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


router = ErrorAwareRouter(
    prefix="/events", 
    tags=["Admin Events"],
    route_class=DishkaErrorAwareRoute,
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=EventResponse,
    error_map=error_map,
)
async def create_event(
    category_id: Annotated[UUID, Form()],
    name: Annotated[str, Form(min_length=2, max_length=32)],
    description: Annotated[str, Form(min_length=2, max_length=256)],
    images: Annotated[list[UploadFile], File(min_length=1, max_length=12)],
    handler: FromDishka[CreateEventCommandHandler],
    mapper: FromDishka[EventMapper],
) -> EventResponse:
    event_data = CreateEventForm(
        category_id=category_id,
        name=name,
        description=description,
        images=images,
    )
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
    name: Annotated[str, Form(min_length=2, max_length=32)],
    description: Annotated[str, Form(min_length=2, max_length=256)],
    image_ids: Annotated[list[UUID], Form(min_length=1, max_length=12)],
    images: Annotated[list[UploadFile], File(min_length=1, max_length=12)],
    orders: Annotated[
        list[Annotated[int, Field(ge=0, le=11)]],
        Form(min_length=1, max_length=12),
    ],
    handler: FromDishka[UpdateEventCommandHandler],
    mapper: FromDishka[EventMapper],
) -> EventResponse:
    try:
        event_data = UpdateEventForm(
            name=name,
            description=description,
            image_ids=image_ids,
            images=images,
            orders=orders,
        )
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.errors(),
        ) from exc

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
