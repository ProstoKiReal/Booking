from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from booking_api.application.interfaces.repositories import CategoryRepo
from booking_api.infrastructure.database.repositories.category_repo import AlchemyCategoryRepo


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def category_repo(self, session: AsyncSession) -> CategoryRepo:
        return AlchemyCategoryRepo(session=session)
