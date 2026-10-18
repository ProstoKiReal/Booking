from dishka import Provider, Scope, provide

from catalog_api.presentation.http.v1.mappers.category import (
    CreateCategoryMapper,
    GetCategoryMapper,
    GetListCategoryMapper,
    UpdateCategoryMapper,
)
from catalog_api.presentation.http.v1.mappers.event import EventMapper
from catalog_api.presentation.http.v1.mappers.list_filters import ListFiltersMapper


class PresentationMappersProvider(Provider):
    scope = Scope.APP

    @provide
    def create_category_mapper(self) -> CreateCategoryMapper:
        return CreateCategoryMapper()

    @provide
    def update_category_mapper(self) -> UpdateCategoryMapper:
        return UpdateCategoryMapper()

    @provide
    def get_category_mapper(self) -> GetCategoryMapper:
        return GetCategoryMapper()

    @provide
    def get_list_category_mapper(self) -> GetListCategoryMapper:
        return GetListCategoryMapper()

    @provide
    def event_mapper(self) -> EventMapper:
        return EventMapper()

    @provide
    def list_filters_mapper(self) -> ListFiltersMapper:
        return ListFiltersMapper()
