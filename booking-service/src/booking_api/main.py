from fastapi import FastAPI

from booking_api.setup import create_fastapi_app, create_dishka

def create_app() -> FastAPI:
    app = create_fastapi_app()
    create_dishka(app)
    return app
