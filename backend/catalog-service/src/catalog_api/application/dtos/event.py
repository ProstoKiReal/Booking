from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateEventRequestDTO:
    category_id: UUID
    name: str
    description: str
    images_data: list[bytes]


@dataclass
class UpdateEventImageDTO:
    id: UUID
    image_data: bytes
    order: int


@dataclass
class UpdateEventRequestDTO:
    name: str
    description: str
    images_data: list[UpdateEventImageDTO]


@dataclass
class EventImageResponseDTO:
    uuid: UUID
    url: str
    order: int


@dataclass
class EventResponseDTO:
    id: UUID
    category_id: UUID
    name: str
    description: str
    images: list[EventImageResponseDTO]


@dataclass
class GetListEventResponseDTO:
    result: list[EventResponseDTO]
