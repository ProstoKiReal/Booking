from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, DishkaRoute


router = APIRouter(prefix="/events", tags=["Events"], route_class=DishkaRoute)


@router.post("/")
async def create_event():
    pass


@router.get("/")
async def get_all_events():
    pass


@router.get("/{event_id}")
async def get_event(event_id: int):
    pass


@router.patch("/{event_id}")
async def update(event_id: int):
    pass


@router.delete("/{event_id}")
async def delete(event_id: int):
    pass
