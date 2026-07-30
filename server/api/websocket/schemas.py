from enum import StrEnum
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict, Field

from domain.value_objects.enums import PlayerSymbol

if TYPE_CHECKING:
    from domain.entities.game import Game


class ClientMessageType(StrEnum):
    MAKE_MOVE = "make_move"
    REMATCH = "rematch"


class ServerMessageType(StrEnum):
    # Presence and moves all reach the client through GAME_UPDATE, which
    # carries the whole board and both players.
    ERROR = "error"
    GAME_UPDATE = "game_update"


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


class GameFullErrorPayload(BaseModel):
    kind: Literal[ServerErrors.GAME_FULL] = ServerErrors.GAME_FULL


class GameFullErrorMessage(BaseMessage[GameFullErrorPayload]):
    type: Literal[ServerMessageType.ERROR] = ServerMessageType.ERROR


class GameNotFoundErrorPayload(BaseModel):
    kind: Literal[ServerErrors.GAME_NOT_FOUND] = ServerErrors.GAME_NOT_FOUND


class GameNotFoundErrorMessage(BaseMessage[GameNotFoundErrorPayload]):
    type: Literal[ServerMessageType.ERROR] = ServerMessageType.ERROR


class GameUpdatePayload(BaseModel):
    board: list[list[str | None]]
    status: str
    current_player: str
    winner: PlayerSymbol | None
    player_x: PlayerPayload | None = None
    player_o: PlayerPayload | None = None


class GameUpdateMessage(BaseMessage[GameUpdatePayload]):
    type: Literal[ServerMessageType.GAME_UPDATE] = ServerMessageType.GAME_UPDATE

    @classmethod
    def from_game(cls, game: "Game") -> "GameUpdateMessage":
        return cls(
            payload=GameUpdatePayload(
                board=game.board.get_grid(),
                status=game.status.value,
                current_player=game.current_player.value,
                winner=game.winner,
                player_x=(
                    PlayerPayload.model_validate(game.player_x)
                    if game.player_x
                    else None
                ),
                player_o=(
                    PlayerPayload.model_validate(game.player_o)
                    if game.player_o
                    else None
                ),
            )
        )


class GenericErrorPayload(BaseModel):
    kind: str = "error"
    message: str


class GenericErrorMessage(BaseMessage[GenericErrorPayload]):
    type: Literal[ServerMessageType.ERROR] = ServerMessageType.ERROR
