from datetime import datetime
from typing import ClassVar
from uuid import UUID

from pydantic import BaseModel, Field

from domain.value_objects.enums import GameMode

ClassicGrid = list[list[str | None]]
UltimateGrid = list[list[ClassicGrid]]


class CreateGameRequest(BaseModel):
    mode: GameMode = GameMode.CLASSIC


class CreateGameResponse(BaseModel):
    id: UUID
    mode: GameMode = GameMode.CLASSIC


class PlayerInfoResponse(BaseModel):
    username: str
    connected: bool


class GameResponse(BaseModel):
    id: UUID
    mode: GameMode = GameMode.CLASSIC
    board: ClassicGrid | UltimateGrid = Field(
        ..., description="3x3 board, or 3x3 of 3x3 boards in ultimate mode"
    )
    current_player: str = Field(..., description="Current player (X or O)")
    status: str = Field(..., description="Game status")
    winner: str | None = Field(None, description="Winner if game is finished")
    meta_board: ClassicGrid | None = Field(None, description="Claimed large cells")
    drawn_boards: list[list[int]] | None = Field(
        None, description="Large cells that finished as a draw"
    )
    active_board: list[int] | None = Field(
        None, description="Large cell the next move must go in; null means anywhere"
    )
    player_x: PlayerInfoResponse | None = None
    player_o: PlayerInfoResponse | None = None
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    ended_at: datetime | None = None

    class Config:
        def __init__(self) -> None:
            self.json_schema_extra = {
                "example": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "board": [["X", "O", None], ["O", "X", None], [None, None, None]],
                    "current_player": "X",
                    "status": "in_progress",
                    "winner": None,
                    "player_x": {
                        "username": "Alice",
                        "connected": True,
                    },
                    "player_o": {
                        "username": "Bob",
                        "connected": True,
                    },
                    "created_at": "2024-01-01T12:00:00",
                    "updated_at": "2024-01-01T12:05:00",
                    "started_at": "2024-01-01T12:01:00",
                    "ended_at": None,
                }
            }


class ErrorResponse(BaseModel):
    detail: str

    class Config:
        json_schema_extra: ClassVar[dict] = {"example": {"detail": "Game not found"}}


class HealthResponse(BaseModel):
    status: str = "healthy"
    service: str = "tic-tac-toe-multiplayer-api"
    version: str = "2.0.0"
    features: list[str] = ["websocket", "multiplayer", "real-time"]
