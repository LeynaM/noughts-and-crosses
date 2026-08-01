import logging
from typing import Any
from uuid import UUID

from fastapi import WebSocket

from api.websocket.handlers.base import WebSocketHandler
from api.websocket.schemas import ClientMessageType, MakeMoveMessage, MakeMovePayload
from domain.value_objects.position import Position, UltimatePosition
from errors import GameError

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
            position = self._to_position(move_msg.payload)

            await self.service.make_move(
                UUID(game_id) if isinstance(game_id, str) else game_id,
                username,
                position,
            )

        except GameError as e:
            # A rule violation. Expected during play, so no traceback.
            await self.send_error(websocket, str(e))
        except ValueError as e:
            await self.send_error(websocket, str(e))
        except Exception as e:
            logger.exception("Unexpected error processing move")
            await self.send_error(websocket, str(e))

    @staticmethod
    def _to_position(payload: MakeMovePayload) -> Position | UltimatePosition:
        if payload.board_row is None or payload.board_col is None:
            return Position(payload.row, payload.col)
        return UltimatePosition(
            Position(payload.board_row, payload.board_col),
            Position(payload.row, payload.col),
        )
