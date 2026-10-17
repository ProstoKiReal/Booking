import asyncio
from uuid import uuid4

from aiobotocore.client import AioBaseClient

from catalog_api.application.interfaces.repositories import ImageStorageRepo


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
        await self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=object_data,
        )
        return self._url_for(key)

    async def save_batch(self, images_data: list[bytes]) -> list[str]:
        sem = asyncio.Semaphore(_MAX_CONCURRENT)
        async with asyncio.TaskGroup() as task_group:
            tasks = [
                task_group.create_task(self._save_with_limit(sem, image_data))
                for image_data in images_data
            ]
        return [task.result() for task in tasks]

    async def delete(self, image_url: str) -> None:
        await self.client.delete_object(
            Bucket=self.bucket,
            Key=self._key_from_url(image_url),
        )

    async def get(self, image_url: str) -> bytes:
        response = await self.client.get_object(
            Bucket=self.bucket,
            Key=self._key_from_url(image_url),
        )
        async with response["Body"] as body:
            return await body.read()

    async def _save_with_limit(self, sem: asyncio.Semaphore, image_data: bytes) -> str:
        async with sem:
            return await self.save(image_data)

    def _url_for(self, key: str) -> str:
        return f"{self.public_endpoint}/{self.bucket}/{key}"

    def _key_from_url(self, image_url: str) -> str:
        prefix = f"{self.public_endpoint}/{self.bucket}/"
        if not image_url.startswith(prefix):
            raise ValueError("Image URL does not belong to this S3 bucket.")

        key = image_url.removeprefix(prefix)
        if not key or "/" in key:
            raise ValueError("Image URL must identify one object in this S3 bucket.")
        return key
