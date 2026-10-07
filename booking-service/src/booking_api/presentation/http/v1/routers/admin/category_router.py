from uuid import UUID

from fastapi import status
from dishka.integrations.fastapi import FromDishka
from fastapi_error_map import ErrorAwareRouter

from booking_api.application.handlers.commands.categories_command_handlers import (
    CreateCategoryCommandHandler,
    UpdateCategoryCommandHandler,
    DeleteCategoryCommandHandler,
)
from booking_api.application.handlers.queries.categories_query_handlers import (
    GetCategoryQueryHandler,
    ListCategoriesQueryHandler,
)
from booking_api.presentation.http.http_route import DishkaErrorAwareRoute
from booking_api.presentation.http.v1.mappers.category import (
    CreateCategoryMapper,
    GetCategoryMapper,
    GetListCategoryMapper,
    UpdateCategoryMapper,
)
from booking_api.presentation.http.v1.schemas.category import (
    CreateCategoryRequest,
    CreateCategoryResponse,
    GetCategoryResponse,
    GetListCategoryResponse,
    UpdateCategoryRequest,
    UpdateCategoryResponse,
)
from booking_api.domain.catalog.errors import (
    CategoryAlreadyExistsError,
    CategoryNameEmptyError,
    CategoryNameTooLongError,
    CategoryNameTooShortError,
    CategoryNotFoundError,
    CategoryOldNameEquivalentNewNameError,
)

error_map = {
    CategoryAlreadyExistsError: status.HTTP_409_CONFLICT,
    CategoryNameTooShortError: status.HTTP_400_BAD_REQUEST,
    CategoryNameTooLongError: status.HTTP_400_BAD_REQUEST,
    CategoryNameEmptyError: status.HTTP_400_BAD_REQUEST,
    CategoryOldNameEquivalentNewNameError: status.HTTP_400_BAD_REQUEST,
    CategoryNotFoundError: status.HTTP_404_NOT_FOUND,
}


router = ErrorAwareRouter(
    prefix="/categories",
    tags=["Categories"],
    route_class=DishkaErrorAwareRoute,
)


@router.get("/", response_model=GetListCategoryResponse)
async def list_categories(
    handler: FromDishka[ListCategoriesQueryHandler],
    mapper: FromDishka[GetListCategoryMapper],
) -> GetListCategoryResponse:
    categories = await handler()
    return mapper.to_response(categories)


@router.get("/{category_id}", response_model=GetCategoryResponse, error_map=error_map)
async def get_category(
    category_id: UUID,
    handler: FromDishka[GetCategoryQueryHandler],
    mapper: FromDishka[GetCategoryMapper],
) -> GetCategoryResponse:
    category = await handler(category_id)
    return mapper.to_response(category)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    error_map=error_map,
)
async def create_category(
    handler: FromDishka[CreateCategoryCommandHandler],
    category_data: CreateCategoryRequest,
    mapper: FromDishka[CreateCategoryMapper],
) -> CreateCategoryResponse:
    data = mapper.to_dto(category_data)
    category = await handler(data)
    return mapper.to_response(category)


@router.patch(
    "/{category_id}",
    status_code=status.HTTP_201_CREATED,
    error_map=error_map,
)
async def update_category(
    category_id: UUID,
    category_data: UpdateCategoryRequest,
    handler: FromDishka[UpdateCategoryCommandHandler],
    mapper: FromDishka[UpdateCategoryMapper],
) -> UpdateCategoryResponse:
    data = mapper.to_dto(category_data)
    category = await handler(category_id, data)
    return mapper.to_response(category)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    error_map=error_map,
)
async def delete_category(
    category_id: UUID,
    handler: FromDishka[DeleteCategoryCommandHandler],
) -> None:
    await handler(category_id)
