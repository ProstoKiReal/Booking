from catalog_api.application.dtos.list_filters import ListFiltersDTO
from catalog_api.presentation.http.v1.schemas.list_filters import ListFilters


class ListFiltersMapper:
    @staticmethod
    def to_dto(filters: ListFilters) -> ListFiltersDTO:
        return ListFiltersDTO(
            offset=filters.offset,
            limit=filters.limit,
            category_id=filters.category_id,
        )
