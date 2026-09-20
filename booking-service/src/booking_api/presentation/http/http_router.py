from fastapi import APIRouter

from booking_api.presentation.http.v1.v1_router import v1_router

http_router = APIRouter(prefix="/api")

routers = [
    v1_router,
]

for router in routers:
    http_router.include_router(router)
