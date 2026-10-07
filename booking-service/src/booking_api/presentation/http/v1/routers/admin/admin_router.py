from fastapi import APIRouter

from booking_api.presentation.http.v1.routers.admin.event_router import router as event_router
from booking_api.presentation.http.v1.routers.admin.category_router import router as category_router


admin_router = APIRouter(
    prefix="/admin", 
    tags=["Admin"],
)

routers = [
    event_router,
    category_router,
]

for router in routers:
    admin_router.include_router(router)
