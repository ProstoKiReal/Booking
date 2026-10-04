from dishka import Provider, Scope, provide

from booking_api.presentation.http.v1.mappers.category import CategoryMapper


class MappersProvider(Provider):
    scope = Scope.APP

    @provide
    def category_mapper(self) -> CategoryMapper:
        return CategoryMapper()
