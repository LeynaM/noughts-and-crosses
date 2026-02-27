import random

from pydantic import BaseModel, Field


class Player(BaseModel):
    player_id: int = Field(...)
    name: str = Field(min_length=1)
    symbol: str = Field(default_factory=lambda: random.choice(["X", "O"]))  # noqa: S311
