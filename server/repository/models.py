from typing import Protocol

from rooms.models import Room


class Item[K](Protocol):
    id: K


class Repository[T: Item[K], K](Protocol):
    def add(self, item: T) -> None: ...

    def get(self) -> list[T] | None: ...

    def get_by_id(self, item_id: K) -> T: ...

    def remove(self, item_id: K) -> None: ...


class InMemoryRepository[T: Item[K], K]:
    def __init__(self) -> None:
        self.items: dict[T[id], T] = {}

    def add(self, item: T) -> None:
        self.items[item.id] = item

    def get(self) -> list[T]:
        return self.items.values()

    def get_by_id(self, item_id: K) -> T | None:
        return self.items.get(item_id, None)

    def remove(self, item_id: K) -> None:
        self.remove(item_id)


class RoomRepository(InMemoryRepository[Room, str]): ...
