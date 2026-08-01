from enum import StrEnum


class PlayerSymbol(StrEnum):
    X = "X"
    O = "O"  # noqa: E741


class GameStatus(StrEnum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    OVER = "over"
    ABANDONED = "abandoned"


class GameMode(StrEnum):
    CLASSIC = "classic"
    ULTIMATE = "ultimate"
