from repository.models import InMemoryRepository, RoomRepository

room_repository: RoomRepository = InMemoryRepository()


def get_room_repository() -> RoomRepository:
    return room_repository
