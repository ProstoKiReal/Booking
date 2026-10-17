from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, Field, model_validator


class CreateEventForm(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    category_id: UUID
    name: str
    description: str
    images: list[UploadFile]


class UpdateEventForm(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    description: str
    image_ids: list[UUID]
    images: list[UploadFile]
    orders: list[int]

    @model_validator(mode="after")
    def validate_image_mapping(self) -> "UpdateEventForm":
        if not (
            len(self.image_ids) == len(self.images) == len(self.orders)
        ):
            raise ValueError(
                "Each uploaded image must have one image ID and one order."
            )

        if any(order < 0 or order > 11 for order in self.orders):
            raise ValueError("Image orders must be between 0 and 11.")

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
