import json
from collections import defaultdict

from fastapi import WebSocket

from custom_types import MessageType


class ClientConnection:
    def __init__(self, client_id: int, websocket: WebSocket) -> None:
        self.id = client_id
        self.websocket = websocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_rooms: dict[str, list[ClientConnection]] = defaultdict(list)

    def connect(
        self,
        client_id: int,
        room_id: str,
        websocket: WebSocket,
    ) -> None:
        client_connection = ClientConnection(client_id, websocket)
        self.active_rooms[room_id].append(client_connection)

    def disconnect(self, client_id: int, room_id: str) -> None:
        if room_id not in self.active_rooms:
            return

        self.active_rooms[room_id] = [
            conn for conn in self.active_rooms[room_id] if conn.id != client_id
        ]

        if len(self.active_rooms[room_id]) == 0:
            del self.active_rooms[room_id]

    async def broadcast_to_room(self, room_id: str, message: str) -> None:
        for client_connection in self.active_rooms[room_id]:
            await client_connection.websocket.send_text(message)

    async def error_response(self, room_id: str, client_id: int, reason: str) -> None:
        client_connection = next(
            conn for conn in self.active_rooms[room_id] if conn.id == client_id
        )
        message = json.dumps(
            {"type": MessageType.ERROR, "payload": {"message": reason}}
        )
        await client_connection.websocket.send_text(message)
