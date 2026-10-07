from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, update

from booking_api.application.interfaces.repositories import CategoryRepo
from booking_api.infrastructure.database.models import CategorySaModel
from booking_api.domain.catalog.entities import Category
from booking_api.domain.catalog.value_objects import CategoryID


class AlchemyCategoryRepo(CategoryRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, category_data: Category) -> Category:
        category = self.to_model(category_data)
        self.session.add(category)
        await self.session.flush()
        await self.session.refresh(category)
        return self.to_domain(category)

    async def exists_by_name(self, name: str) -> bool:
        query = select(CategorySaModel.id).where(CategorySaModel.name == name).limit(1)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def get(self, category_id: CategoryID) -> Category | None:
        query = select(CategorySaModel).where(CategorySaModel.id == category_id.value)
        result = await self.session.execute(query)
        category = result.scalar_one_or_none()
        return self.to_domain(category) if category else None

    async def get_all(self) -> list[Category]:
        query = select(CategorySaModel)
        result = await self.session.execute(query)
        categories = result.scalars().all()
        return [self.to_domain(category) for category in categories]

    async def delete(self, category_id: CategoryID) -> None:
        query = delete(CategorySaModel).where(CategorySaModel.id == category_id.value)
        await self.session.execute(query)

    async def update(self, category: Category) -> Category:
        query = (
            update(CategorySaModel)
            .where(CategorySaModel.id == category.id.value)
            .values(name=category.name)
            .returning(CategorySaModel)
        )
        result = await self.session.execute(query)
        await self.session.flush()
        updated_category = result.scalar_one()
        return self.to_domain(updated_category)

    def to_domain(self, category: CategorySaModel) -> Category:
        return Category(
            id=CategoryID(category.id),
            name=category.name,
        )

    def to_model(self, category: Category) -> CategorySaModel:
        return CategorySaModel(
            id=category.id.value,
            name=category.name,
        )
