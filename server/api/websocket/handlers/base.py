import logging
from abc import ABC, abstractmethod
from typing import Any

from fastapi import WebSocket

from infrastructure.websocket_manager import ConnectionManager
from services.game_service import GameService

logger = logging.getLogger(__name__)


class WebSocketHandler(ABC):
    def __init__(self, service: GameService, manager: ConnectionManager) -> None:
        self.service = service
        self.manager = manager

    @abstractmethod
    async def can_handle(self, message_type: str) -> bool:
        pass

    @abstractmethod
    async def handle(
        self,
        websocket: WebSocket,
        message: dict[str, Any],
        game_id: str,
        username: str,
    ) -> None:
        pass

    async def send_error(self, websocket: WebSocket, error_message: str) -> None:
        await self.manager.send_personal_message(
            {"type": "error", "message": error_message}, websocket
        )
