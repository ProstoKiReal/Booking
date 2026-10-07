from uuid import UUID

from booking_api.application.dtos.category import (
    GetCategoryResponseDTO,
    GetListCategoryResponseDTO,
)
from booking_api.application.interfaces.repositories import CategoryRepo
from booking_api.application.mappers import CategoryMapper
from booking_api.domain.catalog.errors import CategoryNotFoundError
from booking_api.domain.catalog.value_objects import CategoryID


class GetCategoryQueryHandler:
    def __init__(self, category_repo: CategoryRepo, mapper: CategoryMapper):
        self.category_repo = category_repo
        self.mapper = mapper

    async def __call__(self, category_id: UUID) -> GetCategoryResponseDTO:
        category = await self.category_repo.get(CategoryID(category_id))
        if category is None:
            raise CategoryNotFoundError(category_id)
        return self.mapper.to_get_dto(category)


class ListCategoriesQueryHandler:
    def __init__(self, category_repo: CategoryRepo, mapper: CategoryMapper):
        self.category_repo = category_repo
        self.mapper = mapper

    async def __call__(self) -> GetListCategoryResponseDTO:
        categories = await self.category_repo.get_all()
        return self.mapper.to_list_dto(categories)
