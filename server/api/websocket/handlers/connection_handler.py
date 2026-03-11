import logging
from uuid import UUID

from fastapi import WebSocket

from api.websocket.schemas import ServerMessageType
from infrastructure.websocket_manager import ConnectionManager
from services.game_service import GameService

logger = logging.getLogger(__name__)


class ConnectionHandler:
    def __init__(self, service: GameService, manager: ConnectionManager) -> None:
        self.service = service
        self.manager = manager

    async def handle_game_connection(
        self, websocket: WebSocket, game_id: UUID, username: str
    ) -> bool:
        await self.manager.connect(websocket, game_id, username)

        game = await self.service.get_game(game_id)

        if not game:
            await self.manager.send_personal_message(
                {"type": ServerMessageType.ERROR, "message": "Game not found"},
                websocket,
            )
            return False

        if not game.is_player_in_game(username):
            if game.is_full():
                await self.manager.send_personal_message(
                    {"type": ServerMessageType.ERROR, "message": "Game is full"},
                    websocket,
                )
                return False

            player_role = game.add_player(username)
            await self.service.update_game(game)

            await self.manager.broadcast_to_game(
                {
                    "type": ServerMessageType.PLAYER_JOINED,
                    "game": game.to_dict(),
                    "player_role": player_role.value,
                },
                game_id,
            )

        player_role = game.get_player_role(username)
        await self.manager.send_personal_message(
            {
                "type": ServerMessageType.GAME_JOINED,
                "game": game.to_dict(),
                "your_role": player_role.value if player_role else None,
            },
            websocket,
        )

        if player_role:
            await self.service.handle_player_reconnect(game_id, username)

        return True
