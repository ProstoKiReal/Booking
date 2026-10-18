from uuid import UUID

from catalog_api.application.dtos.category import (
    GetCategoryResponseDTO,
    GetListCategoryResponseDTO,
)
from catalog_api.application.dtos.list_filters import ListFiltersDTO
from catalog_api.application.interfaces.repositories import CategoryRepo
from catalog_api.application.mappers import CategoryMapper
from catalog_api.domain.catalog.errors import CategoryNotFoundError
from catalog_api.domain.catalog.value_objects import CategoryID


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

    async def __call__(
        self,
        filters: ListFiltersDTO,
    ) -> GetListCategoryResponseDTO:
        categories = await self.category_repo.get_all(filters)
        return self.mapper.to_list_dto(categories)
