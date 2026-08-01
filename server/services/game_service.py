from uuid import UUID

from api.websocket.schemas import GameUpdateMessage
from domain.entities.game import Game
from domain.entities.player import Player
from domain.repositories import GameRepository
from domain.value_objects.enums import GameMode
from domain.value_objects.position import Position, UltimatePosition
from errors import GameNotFoundError
from infrastructure.websocket_manager import ConnectionManager


class GameService:
    def __init__(
        self, repository: GameRepository, connection_manager: ConnectionManager
    ) -> None:
        self._repository = repository
        self._connection_manager = connection_manager

    async def create_game(self, mode: GameMode = GameMode.CLASSIC) -> Game:
        game = Game(mode=mode)
        return await self._repository.create(game)

    async def get_game(self, game_id: UUID) -> Game | None:
        return await self._repository.get(game_id)

    async def game_exists(self, game_id: UUID) -> bool:
        game = await self._repository.get(game_id)
        return bool(game)

    async def update_game(self, game: Game) -> Game:
        return await self._repository.update(game)

    async def make_move(
        self, game_id: UUID, username: str, position: Position | UltimatePosition
    ) -> Game:
        game = await self._repository.get(game_id)
        if not game:
            raise GameNotFoundError(game_id)

        game.make_move(username, position)
        await self._repository.update(game)

        await self._connection_manager.broadcast_to_game(
            GameUpdateMessage.from_game(game), game_id
        )

        return game

    async def rematch(self, game_id: UUID) -> Game:
        game = await self._repository.get(game_id)
        if not game:
            raise GameNotFoundError(game_id)

        game.rematch()
        await self._repository.update(game)

        await self._connection_manager.broadcast_to_game(
            GameUpdateMessage.from_game(game), game_id
        )

        return game

    async def is_game_full(self, game_id: UUID) -> bool:
        game = await self._repository.get(game_id)
        if not game:
            raise GameNotFoundError

        return game.is_full()

    async def is_player_in_game(self, game_id: UUID, username: str) -> bool:
        game = await self._repository.get(game_id)
        if not game:
            raise GameNotFoundError

        return game.is_player_in_game(username)

    async def add_player(self, game_id: UUID, username: str) -> Player:
        game = await self._repository.get(game_id)
        if not game:
            raise GameNotFoundError

        new_player = game.add_player(username)
        await self._repository.update(game)
        return new_player

    async def reconnect_player(self, game_id: UUID, username: str) -> Player:
        game = await self._repository.get(game_id)
        if not game:
            raise GameNotFoundError

        player = game.reconnect_player(username)
        await self._repository.update(game)
        return player

    async def disconnect_player(self, game_id: UUID, username: str) -> Player:
        game = await self._repository.get(game_id)
        if not game:
            raise GameNotFoundError

        player = game.disconnect_player(username)
        await self._repository.update(game)

        return player

    async def delete_game(self, game_id: UUID) -> bool:
        return await self._repository.delete(game_id)

    async def list_games(self) -> list[Game]:
        return await self._repository.list_all()
