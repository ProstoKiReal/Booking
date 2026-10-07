from dishka import Provider, Scope, provide

from booking_api.application.handlers.commands.events_command_handlers import (
    CreateEventCommandHandler,
    UpdateEventCommandHandler,
    DeleteEventCommandHandler,
)
from booking_api.application.handlers.commands.categories_command_handlers import (
    CreateCategoryCommandHandler,
    UpdateCategoryCommandHandler,
    DeleteCategoryCommandHandler,
)
from booking_api.application.handlers.queries.events_query_handlers import (
    ListEventsQueryHandler,
    GetEventQueryHandler,
)
from booking_api.application.handlers.queries.categories_query_handlers import (
    GetCategoryQueryHandler,
    ListCategoriesQueryHandler,
)
from booking_api.application.mappers import CategoryMapper
from booking_api.infrastructure.database.repositories.category_repo import CategoryRepo
from booking_api.infrastructure.database.tx_manager import TXManager


class HandlersProvider(Provider):
    scope = Scope.REQUEST

    # Event
    # Command
    @provide
    def create_event_command_handler(self) -> CreateEventCommandHandler:
        return CreateEventCommandHandler()

    @provide
    def update_event_command_handler(self) -> UpdateEventCommandHandler:
        return UpdateEventCommandHandler()

    @provide
    def delete_event_command_handler(self) -> DeleteEventCommandHandler:
        return DeleteEventCommandHandler()

    # Query
    @provide
    def list_events_query_handler(self) -> ListEventsQueryHandler:
        return ListEventsQueryHandler()

    @provide
    def get_event_query_handler(self) -> GetEventQueryHandler:
        return GetEventQueryHandler()

    @provide
    def get_category_query_handler(
        self,
        category_repo: CategoryRepo,
        mapper: CategoryMapper,
    ) -> GetCategoryQueryHandler:
        return GetCategoryQueryHandler(category_repo, mapper)

    @provide
    def list_categories_query_handler(
        self,
        category_repo: CategoryRepo,
        mapper: CategoryMapper,
    ) -> ListCategoriesQueryHandler:
        return ListCategoriesQueryHandler(category_repo, mapper)

    # Category
    # Command
    @provide
    def create_category_command_handler(
        self,
        category_repo: CategoryRepo,
        tx_manager: TXManager,
        mapper: CategoryMapper,
    ) -> CreateCategoryCommandHandler:
        return CreateCategoryCommandHandler(
            category_repo=category_repo,
            tx_manager=tx_manager,
            mapper=mapper,
        )

    @provide
    def update_category_command_handler(
        self,
        category_repo: CategoryRepo,
        tx_manager: TXManager,
        mapper: CategoryMapper,
    ) -> UpdateCategoryCommandHandler:
        return UpdateCategoryCommandHandler(
            category_repo=category_repo,
            tx_manager=tx_manager,
            mapper=mapper,
        )

    @provide
    def delete_category_command_handler(
        self,
        category_repo: CategoryRepo,
        tx_manager: TXManager,
    ) -> DeleteCategoryCommandHandler:
        return DeleteCategoryCommandHandler(
            category_repo=category_repo,
            tx_manager=tx_manager,
        )
