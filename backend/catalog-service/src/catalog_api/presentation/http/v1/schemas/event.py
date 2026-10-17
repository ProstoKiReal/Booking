from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel, Field


class CreateEventRequest(BaseModel):
    category_id: UUID
    name: str = Field(..., min_length=2, max_length=32)
    description: str = Field(..., min_length=2, max_length=256)
    images: list[UploadFile] = Field(..., min_items=1, max_items=12)


class CreateImageResponse(BaseModel):
    uuid: UUID
    order: int = Field(..., ge=0, le=11)


class CreateEventResponse(BaseModel):
    id: UUID
    category_id: UUID
    name: str
    description: str
    images: list[CreateImageResponse]


class UpdateImageRequest(BaseModel):
    id: UUID
    image: UploadFile
    order: int = Field(..., ge=0, le=11)


class UpdateEventRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=32)
    description: str = Field(..., min_length=2, max_length=256)
    images: list[UpdateImageRequest] = Field(..., min_items=1, max_items=12)


class GetEventResponse(BaseModel):
    id: UUID
    category_id: UUID
    name: str
    description: str
    images: list[CreateImageResponse]


class GetListEventResponse(BaseModel):
    id: UUID
    category_id: UUID
    name: str
    description: str
    images: list[CreateImageResponse]
