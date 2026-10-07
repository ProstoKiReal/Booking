from dishka import Provider, Scope, provide

from booking_api.application.mappers import CategoryMapper


class ApplicationMappersProvider(Provider):
    scope = Scope.APP

    @provide
    def category_mapper(self) -> CategoryMapper:
        return CategoryMapper()
