import json
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
)

from connections.models import ConnectionManager
from custom_types import MessageType
from dependencies import get_room_repository
from errors import MessageError
from players.models import Player
from repository.models import RoomRepository
from rooms.models import Room
from rooms.router import router as room_router


@asynccontextmanager
async def lifespan(_app: FastAPI):  # noqa: ANN201
    room_repo = get_room_repository()
    test_room = Room("test")
    room_repo.add(test_room)
    yield
    room_repo.remove(test_room)


app = FastAPI(lifespan=lifespan)
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

    connection_manager.connect(client_id, room_id, websocket)
    try:
        while True:
            try:
                message = await websocket.receive_text()
                data = json.loads(message)

                if "type" not in data:
                    raise MessageError("Missing message type")  # noqa: TRY301, TRY003, EM101

                match data["type"]:
                    case MessageType.READY:
                        player = Player(
                            player_id=client_id, name=data["payload"]["name"]
                        )
                        room.add_player(player)
                    case _:
                        raise MessageError("Invalid message type")  # noqa: TRY301, TRY003, EM101

                response = {
                    "type": MessageType.UPDATE,
                    "payload": {
                        "status": room.status,
                        "board": str(room.board),
                        "turn": room.active_player.player_id,
                        "winner": room.winner,
                        "players": str(room.players),
                    },
                }
                await connection_manager.broadcast_to_room(
                    room_id, json.dumps(response)
                )
            except json.JSONDecodeError:
                await connection_manager.error_response(
                    room_id, client_id, "Invalid JSON"
                )
            except MessageError as e:
                await connection_manager.error_response(room_id, client_id, e.message)
    except WebSocketDisconnect:
        connection_manager.disconnect(client_id, room_id)
        room.remove_player(client_id)
