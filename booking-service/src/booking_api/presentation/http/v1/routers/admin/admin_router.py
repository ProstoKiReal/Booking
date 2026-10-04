from fastapi import APIRouter

from booking_api.presentation.http.v1.routers.admin.event_router import router as event_router


admin_router = APIRouter(
    prefix="/admin", 
    tags=["Admin"],
)

routers = [
    event_router,
]

for router in routers:
    admin_router.include_router(router)
