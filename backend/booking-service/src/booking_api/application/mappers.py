from booking_api.application.dtos.category import (
    CategoryName,
    CreateCategoryResponseDTO,
    GetCategoryResponseDTO,
    GetListCategoryResponseDTO,
    UpdateCategoryResponseDTO,
)
from booking_api.domain.catalog.entities import Category
from booking_api.domain.catalog.value_objects import CategoryID


class CategoryMapper:
    def to_domain(
        self,
        category_data: CategoryName,
        category_id: CategoryID | None = None,
    ) -> Category:
        return Category(
            id=category_id or CategoryID.new(),
            name=category_data.name,
        )

    def to_dto(self, category: Category) -> CreateCategoryResponseDTO:
        return CreateCategoryResponseDTO(
            id=category.id.value,
            name=category.name,
        )

    def to_update_dto(self, category: Category) -> UpdateCategoryResponseDTO:
        return UpdateCategoryResponseDTO(
            id=category.id.value,
            name=category.name,
        )

    def to_get_dto(self, category: Category) -> GetCategoryResponseDTO:
        return GetCategoryResponseDTO(
            id=category.id.value,
            name=category.name,
        )

    def to_list_dto(self, categories: list[Category]) -> GetListCategoryResponseDTO:
        return GetListCategoryResponseDTO(
            result=[self.to_get_dto(category) for category in categories]
        )
