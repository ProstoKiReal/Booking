from booking_api.application.dtos.category import CategoryCreateDTO, CategoryDTO
from booking_api.application.interfaces.repositories import CategoryRepo
from booking_api.domain.catalog.entities import Category
from booking_api.domain.catalog.value_objects import CategoryID
from booking_api.infrastructure.database.tx_manager import TXManager


class CreateCategoryCommandHandler:
    def __init__(
        self, 
        category_repo: CategoryRepo,
        tx_manager: TXManager,
    ):
        self.category_repo = category_repo
        self.tx_manager = tx_manager

    async def __call__(self, category_data: CategoryCreateDTO) -> CategoryDTO:
        category = self._to_domain(category_data)
        async with self.tx_manager:
            unique = await self.category_repo.exists_by_name(category.name)
            category.is_unique(unique)
            created_category = await self.category_repo.create(category)
        return self._to_dto(created_category)

    def _to_domain(self, category_data: CategoryCreateDTO) -> Category:
        return Category(
            id=CategoryID.new(),
            name=category_data.name,
        )

    def _to_dto(self, category: Category) -> CategoryDTO:
        return CategoryDTO(
            id=category.id.value,
            name=category.name,
        )

class UpdateCategoryCommandHandler:
    def __init__(
        self, 
        category_repo: CategoryRepo,
    ):
        self.category_repo = category_repo

    async def __call__(self, category_id: int, category_data: CategoryDTO):
        return await self.category_repo.update(category_id, category_data)


class DeleteCategoryCommandHandler:
    def __init__(
        self, 
        category_repo: CategoryRepo,
    ):
        self.category_repo = category_repo
    
    async def __call__(self, category_id: int):
        return await self.category_repo.delete(category_id)
