import asyncio
import logging
from uuid import UUID

from fastapi import WebSocket

from api.websocket.schemas import (
    GameFullErrorMessage,
    GameNotFoundErrorMessage,
    PlayerJoinedMessage,
    PlayerPayload,
    PlayerReconnectedMessage,
)
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
        await asyncio.sleep(0.1)

        game_exists = await self.service.game_exists(game_id)
        if not game_exists:
            await self.manager.send_personal_message(
                GameNotFoundErrorMessage(),
                websocket,
            )
            return False

        is_player_in_game = await self.service.is_player_in_game(game_id, username)
        if is_player_in_game:
             player = await self.service.reconnect_player(game_id, username)
             await self.manager.broadcast_to_game(
                PlayerReconnectedMessage(payload=PlayerPayload.model_validate(player)),
                game_id,
             )
             return True

        is_game_full = await self.service.is_game_full(game_id)
        if is_game_full:
            await self.manager.send_personal_message(
                    GameFullErrorMessage(),
                    websocket,
                )
            return False

        new_player = await self.service.add_player(game_id, username)
        await self.manager.broadcast_to_game(
            PlayerJoinedMessage(payload=PlayerPayload.model_validate(new_player)),
            game_id,
        )
        return True
