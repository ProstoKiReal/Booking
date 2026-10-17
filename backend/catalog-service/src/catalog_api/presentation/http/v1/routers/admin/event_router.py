from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka

from catalog_api.presentation.http.http_route import DishkaRoute
from catalog_api.application.handlers.commands.events_command_handlers import (
    CreateEventCommandHandler,
    UpdateEventCommandHandler,
    DeleteEventCommandHandler,
)
from catalog_api.presentation.http.v1.schemas.event import (
    CreateEventRequest,
    CreateEventResponse,
    UpdateEventRequest,
)


router = APIRouter(
    prefix="/events", 
    tags=["Admin Events"],
    route_class=DishkaRoute,
)


@router.post("/")
async def create_event(
    event_data: CreateEventRequest,
    handler: FromDishka[CreateEventCommandHandler],
):
    return await handler()


@router.patch("/{event_id}")
async def update(event_id: int, handler: FromDishka[UpdateEventCommandHandler]):
    return await handler()


@router.delete("/{event_id}")
async def delete(event_id: int, handler: FromDishka[DeleteEventCommandHandler]):
    return await handler()
