from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from domain.value_objects.enums import PlayerSymbol


class ClientMessageType(StrEnum):
    MAKE_MOVE = "make_move"
    REMATCH = "rematch"


class ServerMessageType(StrEnum):
    PLAYER_JOINED = "player_joined"
    MOVE_MADE = "move_made"
    GAME_ENDED = "game_ended"
    PLAYER_DISCONNECTED = "player_disconnected"
    PLAYER_RECONNECTED = "player_reconnected"
    ERROR = "error"

class ServerErrors(StrEnum):
    GAME_FULL = "game_full"
    GAME_NOT_FOUND = "game_not_found"

class BaseMessage[T](BaseModel):
    type: ClientMessageType | ServerMessageType
    payload: T


class MakeMovePayload(BaseModel):
    row: int = Field(..., ge=0, le=2)
    col: int = Field(..., ge=0, le=2)


class MakeMoveMessage(BaseMessage[MakeMovePayload]):
    type: Literal[ClientMessageType.MAKE_MOVE] = ClientMessageType.MAKE_MOVE


class RematchMessage(BaseMessage[None]):
    type: Literal[ClientMessageType.REMATCH] = ClientMessageType.REMATCH

class PlayerPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    symbol: PlayerSymbol
    connected: bool

class PlayerJoinedMessage(BaseMessage[PlayerPayload]):
    type: Literal[ServerMessageType.PLAYER_JOINED] = ServerMessageType.PLAYER_JOINED

class PlayerReconnectedMessage(BaseMessage[PlayerPayload]):
    type: Literal[ServerMessageType.PLAYER_RECONNECTED] = ServerMessageType.PLAYER_RECONNECTED

class GameFullErrorPayload(BaseModel):
    kind: ServerErrors.GAME_FULL

class GameFullErrorMessage(BaseMessage[GameFullErrorPayload]):
    type: Literal[ServerMessageType.ERROR] = ServerMessageType.ERROR

class GameNotFoundErrorPayload(BaseModel):
    kind: ServerErrors.GAME_NOT_FOUND

class GameNotFoundErrorMessage(BaseMessage[GameFullErrorPayload]):
    type: Literal[ServerMessageType.ERROR] = ServerMessageType.ERROR
