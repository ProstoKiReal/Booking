from dishka import Provider, Scope, provide

from catalog_api.application.mappers import CategoryMapper, EventMapper


class ApplicationMappersProvider(Provider):
    scope = Scope.APP

    @provide
    def category_mapper(self) -> CategoryMapper:
        return CategoryMapper()

    @provide
    def event_mapper(self) -> EventMapper:
        return EventMapper()
