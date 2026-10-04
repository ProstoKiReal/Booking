from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, DishkaRoute


router = APIRouter(
    prefix="/events", 
    tags=["Events"], 
    route_class=DishkaRoute,
)


@router.get("/")
async def get_all_events():
    pass


@router.get("/{event_id}")
async def get_event(event_id: int):
    pass
