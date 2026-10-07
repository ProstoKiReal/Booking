from fastapi import APIRouter

from booking_api.presentation.http.v1.routers.public.event_router import router as event_router


public_router = APIRouter(prefix="/public", tags=["Public"])

routers = [
    event_router,
]

for router in routers:
    public_router.include_router(router)
