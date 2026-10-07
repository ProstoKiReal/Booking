from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from booking_api.application.handlers.commands.events_command_handlers import (
    CreateEventCommandHandler,
    UpdateEventCommandHandler,
    DeleteEventCommandHandler,
)


router = APIRouter(
    prefix="/events", 
    tags=["Admin Events"],
    route_class=DishkaRoute,
)


@router.post("/")
async def create_event(handler: FromDishka[CreateEventCommandHandler]):
    return await handler()


@router.patch("/{event_id}")
async def update(event_id: int, handler: FromDishka[UpdateEventCommandHandler]):
    return await handler()


@router.delete("/{event_id}")
async def delete(event_id: int, handler: FromDishka[DeleteEventCommandHandler]):
    return await handler()
