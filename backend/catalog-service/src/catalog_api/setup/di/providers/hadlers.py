from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

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
from catalog_api.application.interfaces.repositories import (
    CategoryRepo,
    EventRepo,
    ImageRepo,
    ImageStorageRepo,
)
from catalog_api.application.interfaces.services import ImageCleanup
from catalog_api.application.mappers import CategoryMapper, EventMapper


class HandlersProvider(Provider):
    scope = Scope.REQUEST

    # Event
    # Command
    @provide
    def create_event_command_handler(
        self,
        event_repo: EventRepo,
        category_repo: CategoryRepo,
        image_storage_repo: ImageStorageRepo,
        image_cleanup: ImageCleanup,
        session: AsyncSession,
        mapper: EventMapper,
    ) -> CreateEventCommandHandler:
        return CreateEventCommandHandler(
            event_repo=event_repo,
            category_repo=category_repo,
            image_storage_repo=image_storage_repo,
            image_cleanup=image_cleanup,
            session=session,
            mapper=mapper,
        )

    @provide
    def update_event_command_handler(
        self,
        event_repo: EventRepo,
        image_repo: ImageRepo,
        image_storage_repo: ImageStorageRepo,
        image_cleanup: ImageCleanup,
        session: AsyncSession,
        mapper: EventMapper,
    ) -> UpdateEventCommandHandler:
        return UpdateEventCommandHandler(
            event_repo=event_repo,
            image_repo=image_repo,
            image_storage_repo=image_storage_repo,
            image_cleanup=image_cleanup,
            session=session,
            mapper=mapper,
        )

    @provide
    def delete_event_command_handler(
        self,
        event_repo: EventRepo,
        session: AsyncSession,
    ) -> DeleteEventCommandHandler:
        return DeleteEventCommandHandler(
            event_repo=event_repo,
            session=session,
        )

    # Query
    @provide
    def list_events_query_handler(
        self,
        event_repo: EventRepo,
        mapper: EventMapper,
    ) -> ListEventsQueryHandler:
        return ListEventsQueryHandler(
            event_repo=event_repo,
            mapper=mapper,
        )

    @provide
    def get_event_query_handler(
        self,
        event_repo: EventRepo,
        mapper: EventMapper,
    ) -> GetEventQueryHandler:
        return GetEventQueryHandler(
            event_repo=event_repo,
            mapper=mapper,
        )

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
        session: AsyncSession,
        mapper: CategoryMapper,
    ) -> CreateCategoryCommandHandler:
        return CreateCategoryCommandHandler(
            category_repo=category_repo,
            session=session,
            mapper=mapper,
        )

    @provide
    def update_category_command_handler(
        self,
        category_repo: CategoryRepo,
        session: AsyncSession,
        mapper: CategoryMapper,
    ) -> UpdateCategoryCommandHandler:
        return UpdateCategoryCommandHandler(
            category_repo=category_repo,
            session=session,
            mapper=mapper,
        )

    @provide
    def delete_category_command_handler(
        self,
        category_repo: CategoryRepo,
        session: AsyncSession,
    ) -> DeleteCategoryCommandHandler:
        return DeleteCategoryCommandHandler(
            category_repo=category_repo,
            session=session,
        )
