import json
import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect

from api.websocket.handlers.connection_handler import ConnectionHandler
from api.websocket.handlers.move_handler import MoveHandler
from dependencies import get_connection_manager, get_game_service
from infrastructure.websocket_manager import ConnectionManager
from services.game_service import GameService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/ws/game/{game_id}")
async def websocket_game_endpoint(
    websocket: WebSocket,
    game_id: UUID,
    username: str = Query(..., description="Unique username"),
    service: Annotated[GameService, Depends(get_game_service)] = None,
    manager: Annotated[ConnectionManager, Depends(get_connection_manager)] = None,
) -> None:
    connection_handler = ConnectionHandler(service, manager)
    move_handler = MoveHandler(service, manager)

    handlers = [move_handler]

    try:
        success = await connection_handler.handle_game_connection(
            websocket, game_id, username
        )

        if not success:
            return

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            message_type = message.get("type")

            handled = False
            for handler in handlers:
                if await handler.can_handle(message_type):
                    await handler.handle(websocket, message, str(game_id), username)
                    handled = True
                    break

            if not handled:
                logger.warning("Unhandled message type: %s", message_type)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await service.handle_player_disconnect(game_id, username)

    except Exception:
        logger.exception("WebSocket error: %s")
        manager.disconnect(websocket)
        await service.handle_player_disconnect(game_id, username)
