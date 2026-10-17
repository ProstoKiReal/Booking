from uuid import UUID

from dishka.integrations.fastapi import FromDishka
from fastapi import status
from fastapi_error_map import ErrorAwareRouter

from catalog_api.application.handlers.queries.events_query_handlers import (
    ListEventsQueryHandler,
    GetEventQueryHandler,
)
from catalog_api.domain.catalog.errors import EventNotFoundError
from catalog_api.presentation.http.http_route import DishkaErrorAwareRoute
from catalog_api.presentation.http.v1.mappers.event import EventMapper
from catalog_api.presentation.http.v1.schemas.event import (
    EventResponse,
    GetListEventResponse,
)


router = ErrorAwareRouter(
    prefix="/events", 
    tags=["Public Events"], 
    route_class=DishkaErrorAwareRoute,
)

error_map = {
    EventNotFoundError: status.HTTP_404_NOT_FOUND,
}


@router.get("/", response_model=GetListEventResponse)
async def get_all_events(
    handler: FromDishka[ListEventsQueryHandler],
    mapper: FromDishka[EventMapper],
) -> GetListEventResponse:
    res = await handler()
    return mapper.to_list_response(res)


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    error_map=error_map,
)
async def get_event(
    event_id: UUID,
    handler: FromDishka[GetEventQueryHandler],
    mapper: FromDishka[EventMapper],
) -> EventResponse:
    res = await handler(event_id)
    return mapper.to_response(res)
