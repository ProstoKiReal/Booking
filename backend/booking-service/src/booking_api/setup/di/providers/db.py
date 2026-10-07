from typing import AsyncIterable

from sqlalchemy.ext.asyncio import AsyncSession
from dishka import Provider, Scope, provide

from booking_api.infrastructure.database.connection import session_factory


class DBProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def session(self) -> AsyncIterable[AsyncSession]:
        async with session_factory() as session:
            yield session
