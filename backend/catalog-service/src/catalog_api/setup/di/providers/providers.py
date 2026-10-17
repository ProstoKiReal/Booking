from typing import Iterable

from dishka import Provider

from catalog_api.setup.di.providers import (
    TXManagerProvoder,
    DBProvider,
    HandlersProvider,
    S3Provider,
    ApplicationMappersProvider,
    PresentationMappersProvider,
    RepositoriesProvider,
)


def get_providers() -> Iterable[Provider]:
    return (
        TXManagerProvoder(),
        DBProvider(),
        S3Provider(),
        RepositoriesProvider(),
        HandlersProvider(),
        PresentationMappersProvider(),
        ApplicationMappersProvider(),
    )
