from typing import Iterable

from dishka import Provider

from catalog_api.setup.di.providers import (
    DBProvider,
    HandlersProvider,
    S3Provider,
    ApplicationMappersProvider,
    PresentationMappersProvider,
    RepositoriesProvider,
    ServicesProvider,
)


def get_providers() -> Iterable[Provider]:
    return (
        DBProvider(),
        S3Provider(),
        RepositoriesProvider(),
        ServicesProvider(),
        HandlersProvider(),
        PresentationMappersProvider(),
        ApplicationMappersProvider(),
    )
