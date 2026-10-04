from dataclasses import dataclass
from uuid import UUID


@dataclass
class CategoryCreateDTO:
    name: str


@dataclass
class CategoryDTO:
    id: UUID
    name: str
