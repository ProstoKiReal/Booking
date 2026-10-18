import asyncio
from uuid import uuid4

from aiobotocore.client import AioBaseClient
from botocore.exceptions import BotoCoreError, ClientError

from catalog_api.application.interfaces.repositories import ImageStorageRepo
from catalog_api.infrastructure.errors import (
    ImageStorageBatchError,
    ImageStorageError,
    InvalidImageStorageURLError,
)


_MAX_CONCURRENT = 5


class AioBotocoreImageStorageRepo(ImageStorageRepo):
    def __init__(
        self,
        client: AioBaseClient,
        bucket: str,
        public_endpoint: str,
    ) -> None:
        self.client = client
        self.bucket = bucket
        self.public_endpoint = public_endpoint.rstrip("/")

    async def save(self, object_data: bytes) -> str:
        key = uuid4().hex
        try:
            await self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=object_data,
            )
        except (BotoCoreError, ClientError) as error:
            raise ImageStorageError("Failed to upload image to S3.") from error
        return self._url_for(key)

    async def save_batch(self, images_data: list[bytes]) -> list[str]:
        sem = asyncio.Semaphore(_MAX_CONCURRENT)
        tasks: list[asyncio.Task[str]] = []
        try:
            async with asyncio.TaskGroup() as task_group:
                tasks = [
                    task_group.create_task(self._save_with_sem(sem, image_data))
                    for image_data in images_data
                ]
        except* ImageStorageError as errors:
            uploaded_urls = [
                task.result()
                for task in tasks
                if task.done()
                and not task.cancelled()
                and task.exception() is None
            ]
            if uploaded_urls:
                try:
                    await self.delete_batch(uploaded_urls)
                except ImageStorageError as cleanup_error:
                    raise ImageStorageBatchError(
                        "Failed to upload image batch and clean up uploaded images."
                    ) from ExceptionGroup(
                        "Image upload and cleanup both failed.",
                        [errors, cleanup_error],
                    )
            raise ImageStorageBatchError(
                "Failed to upload image batch to S3."
            ) from errors
        return [task.result() for task in tasks]

    async def delete(self, image_url: str) -> None:
        key = self._key_from_url(image_url)
        try:
            await self.client.delete_object(Bucket=self.bucket, Key=key)
        except (BotoCoreError, ClientError) as error:
            raise ImageStorageError("Failed to delete image from S3.") from error

    async def delete_batch(self, image_urls: list[str]) -> None:
        sem = asyncio.Semaphore(_MAX_CONCURRENT)
        try:
            async with asyncio.TaskGroup() as task_group:
                for image_url in image_urls:
                    task_group.create_task(self._delete_with_sem(sem, image_url))
        except* ImageStorageError as errors:
            raise ImageStorageBatchError("Failed to delete image batch from S3.") from errors

    async def get(self, image_url: str) -> bytes:
        key = self._key_from_url(image_url)
        try:
            response = await self.client.get_object(Bucket=self.bucket, Key=key)
            async with response["Body"] as body:
                return await body.read()
        except (BotoCoreError, ClientError) as error:
            raise ImageStorageError("Failed to download image from S3.") from error

    async def _save_with_sem(self, sem: asyncio.Semaphore, image_data: bytes) -> str:
        async with sem:
            return await self.save(image_data)

    async def _delete_with_sem(
        self,
        sem: asyncio.Semaphore,
        image_url: str,
    ) -> None:
        async with sem:
            await self.delete(image_url)

    def _url_for(self, key: str) -> str:
        return f"{self.public_endpoint}/{self.bucket}/{key}"

    def _key_from_url(self, image_url: str) -> str:
        prefix = f"{self.public_endpoint}/{self.bucket}/"
        if not image_url.startswith(prefix):
            raise InvalidImageStorageURLError(
                "Image URL does not belong to this S3 bucket."
            )

        key = image_url.removeprefix(prefix)
        if not key or "/" in key:
            raise InvalidImageStorageURLError(
                "Image URL must identify one object in this S3 bucket."
            )
        return key
