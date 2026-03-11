from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.game import Game


class GameRepository(ABC):
    @abstractmethod
    async def create(self, game: Game) -> Game:
        pass

    @abstractmethod
    async def get(self, game_id: UUID) -> Game | None:
        pass

    @abstractmethod
    async def update(self, game: Game) -> Game:
        pass

    @abstractmethod
    async def delete(self, game_id: UUID) -> bool:
        pass

    @abstractmethod
    async def list_all(self) -> list[Game]:
        pass

    @abstractmethod
    async def find_waiting_game(self) -> Game | None:
        pass
