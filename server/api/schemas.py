from datetime import datetime
from typing import ClassVar
from uuid import UUID

from pydantic import BaseModel, Field


class PlayerInfoResponse(BaseModel):
    username: str
    connected: bool


class GameResponse(BaseModel):
    id: UUID
    board: list[list[str | None]] = Field(
        ..., description="3x3 game board with X, O, or null values"
    )
    current_player: str = Field(..., description="Current player (X or O)")
    status: str = Field(..., description="Game status")
    winner: str | None = Field(None, description="Winner if game is finished")
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


class CreateGameResponse(BaseModel):
    id: UUID


class ErrorResponse(BaseModel):
    detail: str

    class Config:
        json_schema_extra: ClassVar[dict] = {"example": {"detail": "Game not found"}}


class HealthResponse(BaseModel):
    status: str = "healthy"
    service: str = "tic-tac-toe-multiplayer-api"
    version: str = "2.0.0"
    features: list[str] = ["websocket", "multiplayer", "real-time"]
