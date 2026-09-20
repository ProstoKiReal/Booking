from fastapi import APIRouter

from booking_api.presentation.http.v1.event_router import router as event_router


v1_router = APIRouter(prefix="/v1")

routers = [
    event_router,
]

for router in routers:
    v1_router.include_router(router)
