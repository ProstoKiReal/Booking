from uuid import UUID

from booking_api.application.dtos.category import (
    CreateCategoryRequestDTO,
    CreateCategoryResponseDTO,
    UpdateCategoryRequestDTO,
    UpdateCategoryResponseDTO,
)
from booking_api.application.interfaces.repositories import CategoryRepo
from booking_api.application.mappers import CategoryMapper
from booking_api.domain.catalog.errors import CategoryNotFoundError
from booking_api.domain.catalog.value_objects import CategoryID
from booking_api.infrastructure.database.tx_manager import TXManager


class CreateCategoryCommandHandler:
    def __init__(
        self, 
        category_repo: CategoryRepo,
        tx_manager: TXManager,
        mapper: CategoryMapper,
    ):
        self.category_repo = category_repo
        self.tx_manager = tx_manager
        self.mapper = mapper

    async def __call__(
        self,
        category_data: CreateCategoryRequestDTO,
    ) -> CreateCategoryResponseDTO:
        category = self.mapper.to_domain(category_data)
        async with self.tx_manager:
            unique = await self.category_repo.exists_by_name(category.name)
            category.is_unique(unique)
            created_category = await self.category_repo.create(category)
        return self.mapper.to_dto(created_category)


class UpdateCategoryCommandHandler:
    def __init__(
        self, 
        category_repo: CategoryRepo,
        tx_manager: TXManager,
        mapper: CategoryMapper,
    ):
        self.category_repo = category_repo
        self.tx_manager = tx_manager
        self.mapper = mapper

    async def __call__(
        self,
        category_id: UUID,
        category_data: UpdateCategoryRequestDTO,
    ) -> UpdateCategoryResponseDTO:
        category_id_value = CategoryID(category_id)
        category = self.mapper.to_domain(category_data, category_id_value)
        async with self.tx_manager:
            old_category = await self.category_repo.get(category_id_value)
            if old_category is None:
                raise CategoryNotFoundError(category_id)
            category.rename(old_category.name, category.name)
            unique = await self.category_repo.exists_by_name(category.name)
            category.is_unique(unique)
            updated_category = await self.category_repo.update(category)
        return self.mapper.to_update_dto(updated_category)


class DeleteCategoryCommandHandler:
    def __init__(
        self, 
        category_repo: CategoryRepo,
        tx_manager: TXManager,
    ):
        self.category_repo = category_repo
        self.tx_manager = tx_manager
    
    async def __call__(self, category_id: UUID) -> None:
        category_id_value = CategoryID(category_id)
        async with self.tx_manager:
            category = await self.category_repo.get(category_id_value)
            if category is None:
                raise CategoryNotFoundError(category_id)
            await self.category_repo.delete(category_id_value)
