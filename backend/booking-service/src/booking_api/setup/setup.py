from fastapi import FastAPI

from booking_api.presentation.http import http_router


def create_fastapi_app() -> FastAPI:
    app = FastAPI()
    app.include_router(http_router)
    return app
