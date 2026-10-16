from dataclasses import dataclass
from uuid import UUID


@dataclass
class CategoryName:
    name: str


@dataclass
class CategoryID:
    id: UUID


@dataclass
class CreateCategoryRequestDTO(CategoryName):
    pass 


@dataclass
class CreateCategoryResponseDTO(CategoryID, CategoryName):
    pass


@dataclass
class UpdateCategoryRequestDTO(CategoryName):
    pass 


@dataclass
class UpdateCategoryResponseDTO(CategoryID, CategoryName):
    pass


@dataclass
class GetCategoryResponseDTO(CategoryID, CategoryName):
    pass 


@dataclass
class GetListCategoryResponseDTO:
    result: list[GetCategoryResponseDTO]
