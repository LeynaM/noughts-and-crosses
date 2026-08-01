from uuid import UUID


class GameError(Exception):
    """A rule violation. Expected during play, so it is reported without a traceback."""


class GameNotFoundError(GameError):
    def __init__(self, game_id: str | UUID) -> None:
        self.game_id = game_id
        self.message = f"Game {game_id} not found"
        super().__init__(self.message)


class GameFullError(GameError):
    def __init__(self) -> None:
        self.message = "Game is full"
        super().__init__(self.message)


class CannotRematchError(GameError):
    def __init__(self, status: str) -> None:
        self.status = status
        self.message = f"Cannot rematch. Game status: {status}"
        super().__init__(self.message)


class CannotMoveError(GameError):
    def __init__(self, status: str) -> None:
        self.status = status
        self.message = f"Cannot make move. Game status: {status}"
        super().__init__(self.message)


class PlayerNotInGameError(GameError):
    def __init__(self) -> None:
        self.message = "Player not in this game"
        super().__init__(self.message)


class NotYourTurnError(GameError):
    def __init__(self, current_player: str) -> None:
        self.current_player = current_player
        self.message = f"Not your turn. Current player: {self.current_player}"
        super().__init__(self.message)


class InvalidPositionError(GameError):
    def __init__(self) -> None:
        self.message = "Position must be between 0-2 for both row and col"
        super().__init__(self.message)


class PositionOccupiedError(GameError):
    def __init__(self) -> None:
        self.message = "Position already occupied"
        super().__init__(self.message)


class WrongBoardError(GameError):
    def __init__(self, expected: tuple[int, int]) -> None:
        self.expected = expected
        self.message = f"Must play in board {expected}"
        super().__init__(self.message)


class BoardDecidedError(GameError):
    def __init__(self) -> None:
        self.message = "That board is already finished"
        super().__init__(self.message)
