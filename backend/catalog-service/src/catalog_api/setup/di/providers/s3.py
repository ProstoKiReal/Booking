from collections.abc import AsyncIterator

from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session
from botocore.config import Config as BotoConfig
from dishka import Provider, Scope

from catalog_api.setup.config import Config


async def s3_client_provider(config: Config) -> AsyncIterator[AioBaseClient]:
    session = get_session()
    async with session.create_client(
        "s3",
        endpoint_url=config.s3.ENDPOINT_URL,
        aws_access_key_id=config.s3.ACCESS_KEY,
        aws_secret_access_key=config.s3.SECRET_KEY,
        region_name=config.s3.REGION,
        config=BotoConfig(
            signature_version=config.s3.SIGNATURE_VERSION,
            s3={"addressing_style": config.s3.ADDRESSING_STYLE},
        ),
    ) as client:
        yield client


def s3_provider() -> Provider:
    provider = Provider(scope=Scope.APP)
    provider.provide(source=s3_client_provider)
    return provider
