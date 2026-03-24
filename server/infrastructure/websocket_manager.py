import logging
from uuid import UUID

from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

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

    async def send_personal_message(self, message: BaseModel, websocket: WebSocket) -> None:
        data = jsonable_encoder(message)

        try:
            await websocket.send_json(data)
        except Exception:
            logger.exception("Error sending personal message: %s")

    async def broadcast_to_game(
        self, message: BaseModel, game_id: UUID
    ) -> None:
        if game_id not in self._game_connections:
            return

        data = jsonable_encoder(message)

        disconnected = []
        for connection in self._game_connections[game_id]:
            try:
                await connection.send_json(data)
            except Exception:
                logger.exception("Error broadcasting to game %s", game_id)
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)
