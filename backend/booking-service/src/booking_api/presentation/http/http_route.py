from dishka.integrations.fastapi import DishkaRoute
from fastapi_error_map import ErrorAwareRoute


class DishkaErrorAwareRoute(ErrorAwareRoute, DishkaRoute):
    pass
