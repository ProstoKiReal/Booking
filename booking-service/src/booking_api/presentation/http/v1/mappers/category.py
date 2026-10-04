from booking_api.presentation.http.v1.schemas.category import CategoryResponse, CategoryRequest
from booking_api.application.dtos.category import CategoryCreateDTO, CategoryDTO


class CategoryMapper:
    def to_response(self, category: CategoryDTO) -> CategoryResponse:
        return CategoryResponse(
            id=category.id,
            name=category.name,
        )

    def to_dto(self, category: CategoryRequest) -> CategoryCreateDTO:
        return CategoryCreateDTO(
            name=category.name,
        )
