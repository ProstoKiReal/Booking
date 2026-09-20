from typing import Iterable

from dishka import Provider

from booking_api.setup.di.providers.tx_manager import TXManagerProvoder
from booking_api.setup.di.providers.db import DBProvider


def get_providers() -> Iterable[Provider]:
    return (
        TXManagerProvoder(),
        DBProvider(),
    )
