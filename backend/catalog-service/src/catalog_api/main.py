from fastapi import FastAPI
from catalog_api.setup.di import get_providers

from catalog_api.setup import create_fastapi_app, create_dishka


def create_app() -> FastAPI:
    app = create_fastapi_app()
    providers = get_providers()
    create_dishka(app=app, providers=providers)
    return app
