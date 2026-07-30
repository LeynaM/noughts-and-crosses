import logging
from typing import Any
from uuid import UUID

from fastapi import WebSocket

from api.websocket.handlers.base import WebSocketHandler
from api.websocket.schemas import ClientMessageType, RematchMessage
from errors import CannotRematchError

logger = logging.getLogger(__name__)


class RematchHandler(WebSocketHandler):
    async def can_handle(self, message_type: str) -> bool:
        return message_type == ClientMessageType.REMATCH

    async def handle(
        self,
        websocket: WebSocket,
        message: dict[str, Any],
        game_id: str,
        username: str,  # noqa: ARG002
    ) -> None:
        try:
            RematchMessage(**message)

            await self.service.rematch(
                UUID(game_id) if isinstance(game_id, str) else game_id,
            )

        except CannotRematchError as e:
            await self.send_error(websocket, e.message)
        except ValueError as e:
            await self.send_error(websocket, str(e))
        except Exception as e:
            logger.exception("Unexpected error processing rematch")
            await self.send_error(websocket, str(e))
