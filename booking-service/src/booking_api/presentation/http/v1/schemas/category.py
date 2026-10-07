from uuid import UUID

from pydantic import BaseModel


class CategoryName(BaseModel):
    name: str


class CategoryID(BaseModel):
    id: UUID


class CreateCategoryRequest(CategoryName):
    pass 


class CreateCategoryResponse(CategoryID, CategoryName):
    pass


class UpdateCategoryRequest(CategoryName):
    pass 


class UpdateCategoryResponse(CategoryID, CategoryName):
    pass


class GetCategoryResponse(CategoryID, CategoryName):
    pass 


class GetListCategoryResponse(BaseModel):
    result: list[GetCategoryResponse]
