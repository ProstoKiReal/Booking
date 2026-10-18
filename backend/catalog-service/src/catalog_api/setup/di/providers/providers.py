from typing import Iterable

from dishka import Provider

from catalog_api.setup.di.providers import (
    application_mappers_provider,
    db_provider,
    handlers_provider,
    presentation_mappers_provider,
    repositories_provider,
    s3_provider,
    services_provider,
)


def get_providers() -> Iterable[Provider]:
    return (
        db_provider(),
        s3_provider(),
        repositories_provider(),
        services_provider(),
        handlers_provider(),
        presentation_mappers_provider(),
        application_mappers_provider(),
    )
