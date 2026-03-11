from uuid import UUID

from domain.entities.game import Game, GameStatus
from domain.repositories import GameRepository
from errors import GameNotFoundError


class InMemoryGameRepository(GameRepository):
    def __init__(self) -> None:
        self._games: dict[UUID, Game] = {}

    async def create(self, game: Game) -> Game:
        self._games[game.id] = game
        return game

    async def get(self, game_id: UUID) -> Game | None:
        return self._games.get(game_id)

    async def update(self, game: Game) -> Game:
        if game.id not in self._games:
            raise GameNotFoundError(game.id)
        self._games[game.id] = game
        return game

    async def delete(self, game_id: UUID) -> bool:
        if game_id in self._games:
            del self._games[game_id]
            return True
        return False

    async def list_all(self) -> list[Game]:
        return list(self._games.values())

    async def find_waiting_game(self) -> Game | None:
        for game in self._games.values():
            if game.status == GameStatus.WAITING and not game.is_full():
                return game
        return None
