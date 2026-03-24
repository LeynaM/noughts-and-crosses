from enum import StrEnum


class PlayerSymbol(StrEnum):
    X = "X"
    O = "O"  # noqa: E741


class GameStatus(StrEnum):
    WAITING_FOR_OPPONENT = "waiting_for_opponent"
    IN_PROGRESS = "in_progress"
    PLAYER_X_WON = "player_x_won"
    PLAYER_O_WON = "player_o_won"
    DRAW = "draw"
    ABANDONED = "abandoned"
