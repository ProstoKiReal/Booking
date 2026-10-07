from booking_api.presentation.http.v1.schemas.category import (
    CreateCategoryResponse,
    CreateCategoryRequest,
    UpdateCategoryResponse,
    UpdateCategoryRequest,
    GetCategoryResponse,
    GetListCategoryResponse,
)
from booking_api.application.dtos.category import (
    CreateCategoryRequestDTO,
    CreateCategoryResponseDTO,
    UpdateCategoryRequestDTO,
    UpdateCategoryResponseDTO,
    GetCategoryResponseDTO,
    GetListCategoryResponseDTO,
)


class CreateCategoryMapper:
    def to_response(self, category: CreateCategoryResponseDTO) -> CreateCategoryResponse:
        return CreateCategoryResponse(id=category.id, name=category.name)

    def to_dto(self, category: CreateCategoryRequest) -> CreateCategoryRequestDTO:
        return CreateCategoryRequestDTO(name=category.name)


class UpdateCategoryMapper:
    def to_response(self, category: UpdateCategoryResponseDTO) -> UpdateCategoryResponse:
        return UpdateCategoryResponse(id=category.id, name=category.name)

    def to_dto(self, category: UpdateCategoryRequest) -> UpdateCategoryRequestDTO:
        return UpdateCategoryRequestDTO(name=category.name)


class GetCategoryMapper:
    def to_response(self, category: GetCategoryResponseDTO) -> GetCategoryResponse:
        return GetCategoryResponse(id=category.id, name=category.name)


class GetListCategoryMapper:
    def to_response(self, category: GetListCategoryResponseDTO) -> GetListCategoryResponse:
        return GetListCategoryResponse(
            result=[
                GetCategoryResponse(id=item.id, name=item.name)
                for item in category.result
            ]
        )
