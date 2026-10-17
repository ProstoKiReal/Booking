from uuid import UUID

from catalog_api.domain.errors import BaseDomainError

class BaseCatalogDomainError(BaseDomainError):
    pass


class CategoryNameEmptyError(BaseCatalogDomainError):
    def __init__(self) -> None:
        super().__init__("Category name cannot be empty.")


class CategoryNameTooShortError(BaseCatalogDomainError):
    def __init__(self) -> None:
        super().__init__(f"Category name must contain at least 2 characters.")


class CategoryNameTooLongError(BaseCatalogDomainError):
    def __init__(self) -> None:
        super().__init__(f"Category name must contain at most 32 characters.")


class CategoryAlreadyExistsError(BaseCatalogDomainError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Category '{name}' already exists.")


class CategoryNotFoundError(BaseCatalogDomainError):
    def __init__(self, category_id: UUID) -> None:
        super().__init__(f"Category '{category_id}' was not found.")


class CategoryOldNameEquivalentNewNameError(BaseCatalogDomainError):
    def __init__(self, old: str, new) -> None:
        super().__init__(f"Category  old name '{old}' equivalent new name '{new}'.")


class ImageGalleryInvalidOrderError(BaseCatalogDomainError):
    def __init__(self, order: int) -> None:
        super().__init__(f"Image gallery order '{order}' is invalid. Must be in range 0-12.")


class ImageGalleryInvalidCountError(BaseCatalogDomainError):
    def __init__(self, count: int) -> None:
        super().__init__(f"Image gallery count '{count}' is invalid. Must be in range 0-12.")
