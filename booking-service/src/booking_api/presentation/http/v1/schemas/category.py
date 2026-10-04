from uuid import UUID

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class CategoryResponse(CategoryBase):
    id: UUID


class CategoryRequest(CategoryBase):
    pass
