from catalog_api.setup.di.providers.db import db_provider
from catalog_api.setup.di.providers.hadlers import handlers_provider
from catalog_api.setup.di.providers.s3 import s3_provider
from catalog_api.setup.di.providers.repositories import repositories_provider
from catalog_api.setup.di.providers.services import services_provider
from catalog_api.setup.di.providers.mappers.application import application_mappers_provider
from catalog_api.setup.di.providers.mappers.presentation import presentation_mappers_provider


__all__ = [
    "db_provider",
    "handlers_provider",
    "s3_provider",
    "repositories_provider",
    "services_provider",
    "presentation_mappers_provider",
    "application_mappers_provider",
]
