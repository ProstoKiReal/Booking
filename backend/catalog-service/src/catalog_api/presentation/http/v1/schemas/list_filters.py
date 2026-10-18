from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class ListFilters(BaseModel):
    offset: Annotated[int, Field(ge=0)] = 0
    limit: Annotated[int, Field(ge=1, le=100)] = 50
    category_id: UUID | None = None
