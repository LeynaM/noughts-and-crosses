from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class ClientMessageType(str, Enum):
    MAKE_MOVE = "make_move"
    REMATCH = "rematch"


class ServerMessageType(str, Enum):
    GAME_JOINED = "game_joined"
    PLAYER_JOINED = "player_joined"
    MOVE_MADE = "move_made"
    GAME_ENDED = "game_ended"
    PLAYER_DISCONNECTED = "player_disconnected"
    PLAYER_RECONNECTED = "player_reconnected"
    ERROR = "error"


class BaseMessage[T](BaseModel):
    type: ClientMessageType | ServerMessageType
    payload: T


class MakeMovePayload(BaseModel):
    row: int = Field(..., ge=0, le=2)
    col: int = Field(..., ge=0, le=2)


class MakeMoveMessage(BaseMessage[MakeMovePayload]):
    type: Literal[ClientMessageType.MAKE_MOVE] = ClientMessageType.MAKE_MOVE


class RematchMessage(BaseMessage[None | dict]):
    type: Literal[ClientMessageType.REMATCH] = ClientMessageType.REMATCH
    payload: None = None
