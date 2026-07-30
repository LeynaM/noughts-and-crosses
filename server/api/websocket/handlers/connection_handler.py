import asyncio
import logging
from uuid import UUID

from fastapi import WebSocket

from api.websocket.schemas import (
    GameFullErrorMessage,
    GameFullErrorPayload,
    GameNotFoundErrorMessage,
    GameNotFoundErrorPayload,
    GameUpdateMessage,
)
from infrastructure.websocket_manager import ConnectionManager
from services.game_service import GameService

logger = logging.getLogger(__name__)


class ConnectionHandler:
    def __init__(self, service: GameService, manager: ConnectionManager) -> None:
        self.service = service
        self.manager = manager

    async def _broadcast_game(self, game_id: UUID) -> bool:
        game = await self.service.get_game(game_id)
        if not game:
            return False

        await self.manager.broadcast_to_game(GameUpdateMessage.from_game(game), game_id)
        return True

    async def handle_game_connection(
        self, websocket: WebSocket, game_id: UUID, username: str
    ) -> bool:
        await self.manager.connect(websocket, game_id, username)
        await asyncio.sleep(0.1)

        game_exists = await self.service.game_exists(game_id)
        if not game_exists:
            await self.manager.send_personal_message(
                GameNotFoundErrorMessage(payload=GameNotFoundErrorPayload()),
                websocket,
            )
            return False

        is_player_in_game = await self.service.is_player_in_game(game_id, username)
        if is_player_in_game:
            await self.service.reconnect_player(game_id, username)

            # A reconnecting client has no board yet, and reconnecting can move
            # the game out of "abandoned", which the other player needs too.
            return await self._broadcast_game(game_id)

        is_game_full = await self.service.is_game_full(game_id)
        if is_game_full:
            await self.manager.send_personal_message(
                GameFullErrorMessage(payload=GameFullErrorPayload()),
                websocket,
            )
            return False

        await self.service.add_player(game_id, username)
        return await self._broadcast_game(game_id)

    async def handle_game_disconnection(
        self, websocket: WebSocket, game_id: UUID, username: str
    ) -> None:
        self.manager.disconnect(websocket)
        await self.service.disconnect_player(game_id, username)

        # The remaining player needs to see that their opponent has gone, both
        # to learn an in-progress game is now abandoned and to stop being
        # offered a rematch there is nobody left to play.
        await self._broadcast_game(game_id)
