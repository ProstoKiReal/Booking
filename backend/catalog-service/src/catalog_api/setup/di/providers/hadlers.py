from dishka import Provider, Scope

from catalog_api.application.handlers.commands.events_command_handlers import (
    CreateEventCommandHandler,
    UpdateEventCommandHandler,
    DeleteEventCommandHandler,
)
from catalog_api.application.handlers.commands.categories_command_handlers import (
    CreateCategoryCommandHandler,
    UpdateCategoryCommandHandler,
    DeleteCategoryCommandHandler,
)
from catalog_api.application.handlers.queries.events_query_handlers import (
    ListEventsQueryHandler,
    GetEventQueryHandler,
)
from catalog_api.application.handlers.queries.categories_query_handlers import (
    GetCategoryQueryHandler,
    ListCategoriesQueryHandler,
)


def handlers_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(source=CreateEventCommandHandler)
    provider.provide(source=UpdateEventCommandHandler)
    provider.provide(source=DeleteEventCommandHandler)
    provider.provide(source=ListEventsQueryHandler)
    provider.provide(source=GetEventQueryHandler)
    provider.provide(source=GetCategoryQueryHandler)
    provider.provide(source=ListCategoriesQueryHandler)
    provider.provide(source=CreateCategoryCommandHandler)
    provider.provide(source=UpdateCategoryCommandHandler)
    provider.provide(source=DeleteCategoryCommandHandler)
    return provider
