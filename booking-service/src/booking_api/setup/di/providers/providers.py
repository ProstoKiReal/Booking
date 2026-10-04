from typing import Iterable

from dishka import Provider

from booking_api.setup.di.providers.tx_manager import TXManagerProvoder
from booking_api.setup.di.providers.db import DBProvider
from booking_api.setup.di.providers.hadlers import HandlersProvider
from booking_api.setup.di.providers.mappers import MappersProvider
from booking_api.setup.di.providers.repositories import RepositoriesProvider


def get_providers() -> Iterable[Provider]:
    return (
        TXManagerProvoder(),
        DBProvider(),
        RepositoriesProvider(),
        HandlersProvider(),
        MappersProvider(),
    )
