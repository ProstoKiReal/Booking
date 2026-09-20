from fastapi import FastAPI

from dishka.integrations.fastapi import setup_dishka
from dishka import make_async_container

from booking_api.setup.config import Config, config
from booking_api.setup.di.providers.providers import get_providers

def create_dishka(app: FastAPI):
    providers = get_providers()
    container = make_async_container(
        *providers,
        context={Config: config},
    )
    setup_dishka(app=app, container=container)
