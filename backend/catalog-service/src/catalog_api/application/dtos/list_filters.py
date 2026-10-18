from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ListFiltersDTO:
    offset: int
    limit: int
    category_id: UUID | None
