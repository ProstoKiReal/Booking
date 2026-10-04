from fastapi import status
from dishka.integrations.fastapi import FromDishka, inject
from fastapi_error_map import ErrorAwareRouter

from booking_api.application.handlers.commands.categories_command_handlers import (
    CreateCategoryCommandHandler,
    UpdateCategoryCommandHandler,
    DeleteCategoryCommandHandler,
)
from booking_api.presentation.http.v1.mappers.category import CategoryMapper
from booking_api.presentation.http.v1.schemas.category import CategoryRequest
from booking_api.domain.catalog.errors import (
    CategoryAlreadyExistsError, 
    CategoryNameEmptyError, 
    CategoryNameTooLongError, 
    CategoryNameTooShortError,
)


router = ErrorAwareRouter(
    prefix="/categories", 
    tags=["Categories"],
    error_map={
        CategoryAlreadyExistsError: status.HTTP_409_CONFLICT,
        CategoryNameTooShortError: status.HTTP_400_BAD_REQUEST,
        CategoryNameTooLongError: status.HTTP_400_BAD_REQUEST,
        CategoryNameEmptyError: status.HTTP_400_BAD_REQUEST,
    },
)


@router.post("/")
@inject
async def create_category(
    handler: FromDishka[CreateCategoryCommandHandler], 
    category_data: CategoryRequest, 
    mapper: FromDishka[CategoryMapper],
):
    data  = mapper.to_dto(category_data)
    category = await handler(data)
    return mapper.to_response(category)


@router.patch("/{category_id}")
@inject
async def update_category(category_id: int, handler: FromDishka[UpdateCategoryCommandHandler]):
    return await handler()


@router.delete("/{category_id}")
@inject
async def delete_category(category_id: int, handler: FromDishka[DeleteCategoryCommandHandler]):
    return await handler()
