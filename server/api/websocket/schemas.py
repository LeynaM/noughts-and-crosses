from enum import Enum

from pydantic import BaseModel, Field


class ClientMessageType(str, Enum):
    JOIN_GAME = "join_game"
    MAKE_MOVE = "make_move"
    CHAT = "chat"
    REMATCH = "rematch"


class ServerMessageType(str, Enum):
    GAME_JOINED = "game_joined"
    PLAYER_JOINED = "player_joined"
    MOVE_MADE = "move_made"
    GAME_ENDED = "game_ended"
    PLAYER_DISCONNECTED = "player_disconnected"
    PLAYER_RECONNECTED = "player_reconnected"
    ERROR = "error"
    CHAT_MESSAGE = "chat_message"


class PositionMessage(BaseModel):
    row: int = Field(..., ge=0, le=2)
    col: int = Field(..., ge=0, le=2)


class JoinGameMessage(BaseModel):
    type: str = ClientMessageType.JOIN_GAME
    username: str | None


class MakeMoveMessage(BaseModel):
    type: str = ClientMessageType.MAKE_MOVE
    position: PositionMessage


class ChatMessage(BaseModel):
    type: str = ClientMessageType.CHAT
    message: str


class RematchMessage(BaseModel):
    type: str = ClientMessageType.REMATCH
