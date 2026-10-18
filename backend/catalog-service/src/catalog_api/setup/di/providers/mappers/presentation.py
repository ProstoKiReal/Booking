from dishka import Provider, Scope

from catalog_api.presentation.http.v1.mappers.category import (
    CreateCategoryMapper,
    GetCategoryMapper,
    GetListCategoryMapper,
    UpdateCategoryMapper,
)
from catalog_api.presentation.http.v1.mappers.event import EventMapper
from catalog_api.presentation.http.v1.mappers.list_filters import ListFiltersMapper


def presentation_mappers_provider() -> Provider:
    provider = Provider(scope=Scope.APP)
    provider.provide(source=CreateCategoryMapper)
    provider.provide(source=UpdateCategoryMapper)
    provider.provide(source=GetCategoryMapper)
    provider.provide(source=GetListCategoryMapper)
    provider.provide(source=EventMapper)
    provider.provide(source=ListFiltersMapper)
    return provider
