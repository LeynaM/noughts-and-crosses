from uuid import UUID

from domain.entities.game import Game
from domain.entities.player import Player
from domain.repositories import GameRepository
from domain.value_objects.position import Position
from errors import GameNotFoundError
from infrastructure.websocket_manager import ConnectionManager


class GameService:
    def __init__(
        self, repository: GameRepository, connection_manager: ConnectionManager
    ) -> None:
        self._repository = repository
        self._connection_manager = connection_manager

    async def create_game(self) -> Game:
        game = Game()
        return await self._repository.create(game)

    async def get_game(self, game_id: UUID) -> Game | None:
        return await self._repository.get(game_id)

    async def game_exists(self, game_id: UUID) -> bool:
        game = await self._repository.get(game_id)
        return bool(game)

    async def update_game(self, game: Game) -> Game:
        return await self._repository.update(game)

    async def make_move(self, game_id: UUID, username: str, position: Position) -> Game:
        game = await self._repository.get(game_id)
        if not game:
            raise GameNotFoundError(game_id)

        game.make_move(username, position)
        await self._repository.update(game)

        player_role = game.get_player_role(username)
        await self._connection_manager.broadcast_to_game(
            {
                "type": "move_made",
                "game": game.to_dict(),
                "position": {"row": position.row, "col": position.col},
                "player": player_role.value if player_role else None,
            },
            game_id,
        )

        if game.status.value in ["player_x_won", "player_o_won", "draw"]:
            await self._connection_manager.broadcast_to_game(
                {
                    "type": "game_ended",
                    "game": game.to_dict(),
                    "winner": game.winner.value if game.winner else None,
                    "status": game.status.value,
                },
                game_id,
            )

        return game

    async def is_game_full(self, game_id: UUID) -> bool:
        game = await self._repository.get(game_id)
        if not game:
            raise GameNotFoundError

        return game.is_full()

    async def is_player_in_game(self, game_id: UUID, username: str) -> Player:
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

    async def reconnect_player(self, game_id: UUID, username: str) -> None:
        game = await self._repository.get(game_id)
        if not game:
            raise GameNotFoundError

        player = game.reconnect_player(username)
        await self._repository.update(game)
        return player

    async def handle_player_disconnect(self, game_id: UUID, username: str) -> None:
        game = await self._repository.get(game_id)

        if not game:
            return

        game.handle_player_disconnect(username)
        await self._repository.update(game)

        await self._connection_manager.broadcast_to_game(
            {
                "type": "player_disconnected",
                "game": game.to_dict(),
                "username": username,
                "message": "Your opponent has disconnected",
            },
            game_id,
        )

    async def delete_game(self, game_id: UUID) -> bool:
        return await self._repository.delete(game_id)

    async def list_games(self) -> list[Game]:
        return await self._repository.list_all()
