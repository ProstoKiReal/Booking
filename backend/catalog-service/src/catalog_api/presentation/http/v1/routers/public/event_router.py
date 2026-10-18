from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import FromDishka
from fastapi import Query, status
from fastapi_error_map import ErrorAwareRouter

from catalog_api.application.handlers.queries.events_query_handlers import (
    GetEventQueryHandler,
    ListEventsQueryHandler,
)
from catalog_api.domain.catalog.errors import EventNotFoundError
from catalog_api.presentation.http.http_route import DishkaErrorAwareRoute
from catalog_api.presentation.http.v1.mappers.event import EventMapper
from catalog_api.presentation.http.v1.mappers.list_filters import ListFiltersMapper
from catalog_api.presentation.http.v1.schemas.event import (
    EventResponse,
    GetListEventResponse,
)
from catalog_api.presentation.http.v1.schemas.list_filters import ListFilters


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
    filters: Annotated[ListFilters, Query()],
    handler: FromDishka[ListEventsQueryHandler],
    mapper: FromDishka[EventMapper],
    filters_mapper: FromDishka[ListFiltersMapper],
) -> GetListEventResponse:
    res = await handler(filters_mapper.to_dto(filters))
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
