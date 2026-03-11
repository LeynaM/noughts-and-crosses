import json
import logging
from uuid import UUID

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self) -> None:
        self._game_connections: dict[UUID, set[WebSocket]] = {}
        self._connection_info: dict[WebSocket, tuple[UUID, str]] = {}

    async def connect(self, websocket: WebSocket, game_id: UUID, username: str) -> None:
        await websocket.accept()

        if game_id not in self._game_connections:
            self._game_connections[game_id] = set()

        self._game_connections[game_id].add(websocket)
        self._connection_info[websocket] = (game_id, username)

        logger.info("Player %s connected to game %s", username, game_id)

    def disconnect(self, websocket: WebSocket) -> tuple[UUID, str] | None:
        if websocket not in self._connection_info:
            return None

        game_id, username = self._connection_info[websocket]

        if game_id in self._game_connections:
            self._game_connections[game_id].discard(websocket)
            if not self._game_connections[game_id]:
                del self._game_connections[game_id]

        del self._connection_info[websocket]

        logger.info("Player %s disconnected from game %s", username, game_id)
        return game_id, username

    async def send_personal_message(self, message: dict, websocket: WebSocket) -> None:
        try:
            await websocket.send_text(json.dumps(message))
        except Exception:
            logger.exception("Error sending personal message: %s")

    async def broadcast_to_game(
        self, message: dict, game_id: UUID, exclude: WebSocket | None = None
    ) -> None:
        if game_id not in self._game_connections:
            return

        disconnected = []
        for connection in self._game_connections[game_id]:
            if connection == exclude:
                continue

            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                logger.exception("Error broadcasting to game %s", game_id)
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)
