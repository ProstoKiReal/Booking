from typing import Iterable

from fastapi import FastAPI

from dishka.integrations.fastapi import setup_dishka
from dishka import make_async_container, Provider

from catalog_api.setup.config import Config, config


def create_dishka(app: FastAPI, providers: Iterable[Provider]) -> None:
    container = make_async_container(
        *providers,
        context={Config: config},
    )
    setup_dishka(
        app=app, 
        container=container,
    )
