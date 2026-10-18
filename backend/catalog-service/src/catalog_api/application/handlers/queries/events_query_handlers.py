from uuid import UUID

from catalog_api.application.dtos.event import (
    EventResponseDTO,
    GetListEventResponseDTO,
)
from catalog_api.application.dtos.list_filters import ListFiltersDTO
from catalog_api.application.interfaces.repositories import EventRepo
from catalog_api.application.mappers import EventMapper
from catalog_api.domain.catalog.errors import EventNotFoundError
from catalog_api.domain.catalog.value_objects import EventID


class ListEventsQueryHandler:
    def __init__(self, event_repo: EventRepo, mapper: EventMapper) -> None:
        self.event_repo = event_repo
        self.mapper = mapper

    async def __call__(
        self,
        filters: ListFiltersDTO,
    ) -> GetListEventResponseDTO:
        events = await self.event_repo.get_all(filters)
        return self.mapper.to_list_dto(events)


class GetEventQueryHandler:
    def __init__(self, event_repo: EventRepo, mapper: EventMapper) -> None:
        self.event_repo = event_repo
        self.mapper = mapper

    async def __call__(self, event_id: UUID) -> EventResponseDTO:
        event = await self.event_repo.get(EventID(event_id))
        if event is None:
            raise EventNotFoundError(event_id)
        return self.mapper.to_dto(event)
