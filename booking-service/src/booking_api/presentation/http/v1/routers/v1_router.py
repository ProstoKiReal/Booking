from fastapi import APIRouter

from booking_api.presentation.http.v1.routers.admin.admin_router import admin_router
from booking_api.presentation.http.v1.routers.public.public_router import public_router


v1_router = APIRouter(prefix="/v1")

routers = [
    admin_router,
    public_router,
]

for router in routers:
    v1_router.include_router(router)
