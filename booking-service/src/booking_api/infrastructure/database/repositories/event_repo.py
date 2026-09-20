
from sqlalchemy.ext.asyncio import AsyncSession

from booking_api.domain.catalog.repositories import EventRepo
from booking_api.domain.catalog.entities import Event
from booking_api.domain.catalog.value_objects import EventID


class AlchemyEventRepo(EventRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, event_data: Event) -> Event:
        pass

    async def get(self, event_id: EventID) -> Event:
        pass

    async def get_all(self) -> list[Event]: 
        pass

    async def delete(self, event_id: EventID) -> None:
        pass

    async def update(self, event_id: EventID) -> Event:
        pass
