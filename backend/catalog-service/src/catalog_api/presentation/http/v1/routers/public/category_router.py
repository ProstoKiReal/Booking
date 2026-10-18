from typing import Annotated
from uuid import UUID

from fastapi import Query, status
from dishka.integrations.fastapi import FromDishka
from fastapi_error_map import ErrorAwareRouter

from catalog_api.application.handlers.queries.categories_query_handlers import (
    GetCategoryQueryHandler,
    ListCategoriesQueryHandler,
)
from catalog_api.presentation.http.http_route import DishkaErrorAwareRoute
from catalog_api.presentation.http.v1.mappers.category import (
    GetCategoryMapper,
    GetListCategoryMapper,
)
from catalog_api.presentation.http.v1.mappers.list_filters import ListFiltersMapper
from catalog_api.presentation.http.v1.schemas.category import (
    GetCategoryResponse,
    GetListCategoryResponse,
)
from catalog_api.presentation.http.v1.schemas.list_filters import ListFilters
from catalog_api.domain.catalog.errors import (
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
    filters: Annotated[ListFilters, Query()],
    handler: FromDishka[ListCategoriesQueryHandler],
    mapper: FromDishka[GetListCategoryMapper],
    filters_mapper: FromDishka[ListFiltersMapper],
) -> GetListCategoryResponse:
    categories = await handler(filters_mapper.to_dto(filters))
    return mapper.to_response(categories)


@router.get("/{category_id}", response_model=GetCategoryResponse, error_map=error_map)
async def get_category(
    category_id: UUID,
    handler: FromDishka[GetCategoryQueryHandler],
    mapper: FromDishka[GetCategoryMapper],
) -> GetCategoryResponse:
    category = await handler(category_id)
    return mapper.to_response(category)
