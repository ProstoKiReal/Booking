from booking_api.application.interfaces.repositories import EventRepo, CategoryRepo, ImageRepo, ImageStorageRepo

class CreateEventCommandHandler:
    def __init__(self,
        event_repo: EventRepo,
        category_repo: CategoryRepo,
        image_repo: ImageRepo,
        image_storage_repo: ImageStorageRepo,
        ):
        self.event_repo = event_repo
        self.category_repo = category_repo
        self.image_repo = image_repo
        self.image_storage_repo = image_storage_repo

    async def __call__(self, event_data, categories_data, images_data):
        self.event_repo.create()


class UpdateEventCommandHandler:

    async def __call__(self):
        pass


class DeleteEventCommandHandler:
    
    async def __call__(self):
        pass
