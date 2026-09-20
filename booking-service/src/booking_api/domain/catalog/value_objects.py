from dataclasses import dataclass


@dataclass
class EventID:
    id: str | None = None


@dataclass
class CategoryID:
    id: str | None = None


@dataclass
class ImageID:
    id: str | None = None
