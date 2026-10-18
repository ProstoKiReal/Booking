from dishka import Provider, Scope

from catalog_api.application.mappers import CategoryMapper, EventMapper


def application_mappers_provider() -> Provider:
    provider = Provider(scope=Scope.APP)
    provider.provide(source=CategoryMapper)
    provider.provide(source=EventMapper)
    return provider
