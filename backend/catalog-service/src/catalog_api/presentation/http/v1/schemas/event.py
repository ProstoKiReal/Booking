from typing import Annotated
from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, Field, model_validator


class CreateEventForm(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    category_id: UUID
    name: str = Field(min_length=2, max_length=32)
    description: str = Field(min_length=2, max_length=256)
    images: list[UploadFile] = Field(min_length=1, max_length=12)


class UpdateEventForm(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(min_length=2, max_length=32)
    description: str = Field(min_length=2, max_length=256)
    image_ids: list[UUID] = Field(min_length=1, max_length=12)
    images: list[UploadFile] = Field(min_length=1, max_length=12)
    orders: list[Annotated[int, Field(ge=0, le=11)]] = Field(
        min_length=1,
        max_length=12,
    )

    @model_validator(mode="after")
    def validate_image_mapping(self) -> "UpdateEventForm":
        if not (
            len(self.image_ids) == len(self.images) == len(self.orders)
        ):
            raise ValueError(
                "Each uploaded image must have one image ID and one order."
            )

        return self


class EventImageResponse(BaseModel):
    uuid: UUID
    order: int = Field(..., ge=0, le=11)


class EventResponse(BaseModel):
    id: UUID
    category_id: UUID
    name: str
    description: str
    images: list[EventImageResponse]


class GetListEventResponse(BaseModel):
    result: list[EventResponse]
