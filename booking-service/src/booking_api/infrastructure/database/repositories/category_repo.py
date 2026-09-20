from sqlalchemy.ext.asyncio import AsyncSession

from booking_api.domain.catalog.repositories import CategoryRepo
from booking_api.domain.catalog.entities import Category
from booking_api.domain.catalog.value_objects import CategoryID


class AlchemyCategoryRepo(CategoryRepo):
    async def create(self, event_data: Category) -> Category:
        pass

    async def get(self, event_id: CategoryID) -> Category:
        pass

    async def get_all(self) -> list[Category]:
        pass

    async def delete(self, event_id: CategoryID) -> None:
        pass

    async def update(self, event_id: CategoryID) -> Category:
        pass
