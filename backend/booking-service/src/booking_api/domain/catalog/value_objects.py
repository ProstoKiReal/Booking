from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class EventID:
    value: UUID

    @classmethod
    def new(cls) -> Self:
        return cls(uuid4())


@dataclass(frozen=True, slots=True)
class CategoryID:
    value: UUID

    @classmethod
    def new(cls) -> Self:
        return cls(uuid4())


@dataclass(frozen=True, slots=True)
class ImageID:
    value: UUID

    @classmethod
    def new(cls) -> Self:
        return cls(uuid4())
