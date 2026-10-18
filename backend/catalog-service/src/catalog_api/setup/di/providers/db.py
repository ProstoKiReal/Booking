from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession
from dishka import Provider, Scope

from catalog_api.infrastructure.database.connection import session_factory


async def session_provider() -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session


def db_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(source=session_provider)
    return provider
