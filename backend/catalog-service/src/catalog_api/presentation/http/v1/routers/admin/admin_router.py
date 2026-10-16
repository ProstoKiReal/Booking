from fastapi import APIRouter

from catalog_api.presentation.http.v1.routers.admin.event_router import router as event_router
from catalog_api.presentation.http.v1.routers.admin.category_router import router as category_router


admin_router = APIRouter(
    prefix="/admin", 
)

routers = [
    event_router,
    category_router,
]

for router in routers:
    admin_router.include_router(router)
