from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from booking_api.application.handlers.queries.events_query_handlers import (
    ListEventsQueryHandler,
    GetEventQueryHandler,
)


router = APIRouter(
    prefix="/events", 
    tags=["Events"], 
    route_class=DishkaRoute,
)


@router.get("/")
async def get_all_events(handler: FromDishka[ListEventsQueryHandler]):
    return await handler()


@router.get("/{event_id}")
async def get_event(event_id: int, handler: FromDishka[GetEventQueryHandler]):
    return await handler()
