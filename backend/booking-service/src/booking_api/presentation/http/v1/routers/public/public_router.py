from fastapi import APIRouter

from booking_api.presentation.http.v1.routers.public.event_router import router as event_router
from booking_api.presentation.http.v1.routers.public.category_router import router as category_router


public_router = APIRouter(
    prefix="/public", 
)

routers = [
    event_router,
    category_router,
]

for router in routers:
    public_router.include_router(router)
