from typing import Iterable

from dishka import Provider

from booking_api.setup.di.providers import (
    TXManagerProvoder,
    DBProvider,
    HandlersProvider,
    ApplicationMappersProvider,
    PresentationMappersProvider,
    RepositoriesProvider,
)


def get_providers() -> Iterable[Provider]:
    return (
        TXManagerProvoder(),
        DBProvider(),
        RepositoriesProvider(),
        HandlersProvider(),
        PresentationMappersProvider(),
        ApplicationMappersProvider(),
    )
