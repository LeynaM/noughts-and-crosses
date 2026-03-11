import logging
from typing import Any
from uuid import UUID

from fastapi import WebSocket

from api.websocket.handlers.base import WebSocketHandler
from api.websocket.schemas import ClientMessageType, MakeMoveMessage
from domain.value_objects.position import Position

logger = logging.getLogger(__name__)


class MoveHandler(WebSocketHandler):
    async def can_handle(self, message_type: str) -> bool:
        return message_type == ClientMessageType.MAKE_MOVE

    async def handle(
        self,
        websocket: WebSocket,
        message: dict[str, Any],
        game_id: str,
        username: str,
    ) -> None:
        try:
            move_msg = MakeMoveMessage(**message)
            position = Position(row=move_msg.position.row, col=move_msg.position.col)

            # Make the move through the service
            await self.service.make_move(
                UUID(game_id) if isinstance(game_id, str) else game_id,
                username,
                position,
            )

        except ValueError as e:
            await self.send_error(websocket, str(e))
        except Exception as e:
            logger.exception("Unexpected error processing move")
            await self.send_error(websocket, str(e))
