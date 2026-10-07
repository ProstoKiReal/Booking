from sqlalchemy.ext.asyncio import AsyncSession
from dishka import Provider, Scope, provide

from booking_api.infrastructure.database.tx_manager import TXManager


class TXManagerProvoder(Provider):
    scope = Scope.REQUEST

    @provide
    def tx_manager(self, session: AsyncSession) -> TXManager:
        return TXManager(session=session)
