from catalog_api.errors import BaseError


class BaseInfrastructureError(BaseError):
    pass


class ImageStorageError(BaseInfrastructureError):
    pass


class ImageStorageBatchError(ImageStorageError):
    pass


class ImageStorageCleanupError(ImageStorageError):
    pass


class InvalidImageStorageURLError(ImageStorageError):
    pass
