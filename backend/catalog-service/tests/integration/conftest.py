import asyncio

from collections.abc import AsyncIterator
import os
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import pytest_asyncio

from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session
from alembic import command
from alembic.config import Config as AlembicConfig
from botocore.config import Config as BotoConfig
from dishka import Provider, Scope
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from catalog_api.setup.di.providers import (
    application_mappers_provider,
    handlers_provider,
    presentation_mappers_provider,
    repositories_provider,
    services_provider,
)
from catalog_api.setup.di.setup import create_dishka
from catalog_api.setup.setup import create_fastapi_app


@pytest.fixture(scope="session")
def db_config():
    mock = MagicMock()
    mock.HOST = os.getenv("CAT_DB_HOST", "localhost")
    mock.PORT = int(os.getenv("CAT_DB_PORT", "5434"))
    mock.USER = os.environ["CAT_DB_USER"]
    mock.PASSWORD = os.environ["CAT_DB_PASSWORD"]
    mock.DB_NAME = os.getenv("CAT_DB_NAME", "catalog_test")
    mock.URL = f"postgresql+asyncpg://{mock.USER}:{mock.PASSWORD}@{mock.HOST}:{mock.PORT}/{mock.DB_NAME}"
    return mock


@pytest.fixture
def s3_config():
    mock = MagicMock()
    mock.ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "http://localhost:9002")
    mock.ACCESS_KEY = os.environ["S3_ACCESS_KEY"]
    mock.SECRET_KEY = os.environ["S3_SECRET_KEY"]
    mock.REGION = os.getenv("S3_REGION", "us-east-1")
    mock.SIGNATURE_VERSION = os.getenv("S3_SIGNATURE_VERSION", "s3v4")
    mock.ADDRESSING_STYLE = os.getenv("S3_ADDRESSING_STYLE", "path")
    mock.IMAGES_BUCKET = os.getenv("S3_IMAGES_BUCKET", "catalog-images")
    return mock


@pytest.fixture(scope="session")
def db_engine(db_config):
    return create_async_engine(db_config.URL, poolclass=NullPool)


@pytest_asyncio.fixture
async def session_factory(db_engine):
    return async_sessionmaker(
        db_engine,
        expire_on_commit=False,
        autoflush=False,
    )


@pytest_asyncio.fixture
async def session(session_factory):
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def s3_client(s3_config):
    session = get_session()
    async with session.create_client(
        "s3",
        endpoint_url=s3_config.ENDPOINT_URL,
        aws_access_key_id=s3_config.ACCESS_KEY,
        aws_secret_access_key=s3_config.SECRET_KEY,
        region_name=s3_config.REGION,
        config=BotoConfig(
            signature_version=s3_config.SIGNATURE_VERSION,
            s3={"addressing_style": s3_config.ADDRESSING_STYLE},
        ),
    ) as client:
        yield client


@pytest.fixture
def db_provider(session_factory):
    provider = Provider(scope=Scope.REQUEST)

    async def provide_session() -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    provider.provide(source=provide_session)
    return provider


@pytest.fixture
def s3_provider(s3_config):
    provider = Provider(scope=Scope.APP)

    async def provide_s3_client() -> AsyncIterator[AioBaseClient]:
        session = get_session()
        async with session.create_client(
            "s3",
            endpoint_url=s3_config.ENDPOINT_URL,
            aws_access_key_id=s3_config.ACCESS_KEY,
            aws_secret_access_key=s3_config.SECRET_KEY,
            region_name=s3_config.REGION,
            config=BotoConfig(
                signature_version=s3_config.SIGNATURE_VERSION,
                s3={"addressing_style": s3_config.ADDRESSING_STYLE},
            ),
        ) as client:
            yield client

    provider.provide(source=provide_s3_client)
    return provider


@pytest.fixture
def dishka_providers(db_provider, s3_provider):
    return (
        db_provider,
        s3_provider,
        repositories_provider(),
        services_provider(),
        handlers_provider(),
        presentation_mappers_provider(),
        application_mappers_provider(),
    )


@pytest.fixture(scope="session", autouse=True)
def apply_migrations(db_engine):
    service_root = Path(__file__).resolve().parents[2]
    alembic_config = AlembicConfig(str(service_root / "alembic.ini"))
    command.upgrade(alembic_config, "head")
    yield
    asyncio.run(db_engine.dispose())


@pytest.fixture
def app(dishka_providers):
    fastapi_app = create_fastapi_app()
    create_dishka(app=fastapi_app, providers=dishka_providers)
    return fastapi_app


@pytest.fixture
def test_client(app):
    with TestClient(app) as client:
        yield client
