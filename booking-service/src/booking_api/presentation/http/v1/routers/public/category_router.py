from uuid import UUID

from fastapi import status
from dishka.integrations.fastapi import FromDishka
from fastapi_error_map import ErrorAwareRouter

from booking_api.application.handlers.queries.categories_query_handlers import (
    GetCategoryQueryHandler,
    ListCategoriesQueryHandler,
)
from booking_api.presentation.http.http_route import DishkaErrorAwareRoute
from booking_api.presentation.http.v1.mappers.category import (
    GetCategoryMapper,
    GetListCategoryMapper,
)
from booking_api.presentation.http.v1.schemas.category import (
    GetCategoryResponse,
    GetListCategoryResponse,
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
    tags=["Public Categories"],
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
