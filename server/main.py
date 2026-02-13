from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
)

from connections.models import ConnectionManager
from dependencies import get_room_repository
from players.models import Player
from repository.models import RoomRepository
from rooms.router import router as room_router

app = FastAPI()
app.include_router(room_router)

count = 0

connection_manager = ConnectionManager()


@app.websocket("/ws/rooms/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    room_repository: Annotated[RoomRepository, Depends(get_room_repository)],
) -> None:
    await websocket.accept()
    global count  # noqa: PLW0603
    count += 1
    client_id = count
    room = room_repository.get_by_id(room_id)
    if room is None:
        raise WebSocketException(code=4004, reason="Room not found")
    if not room.is_open():
        raise WebSocketException(code=4003, reason="Room is full")

    player = Player(id=client_id)
    room.add_player(player)
    await connection_manager.connect(client_id, room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.broadcast_to_room(
                room_id, f"Client {client_id} said: {data}"
            )
    except WebSocketDisconnect:
        connection_manager.disconnect(client_id, room_id)
        room.remove_player(client_id)
