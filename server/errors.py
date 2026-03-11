from uuid import UUID


class GameNotFoundError(Exception):
    def __init__(self, game_id: str | UUID) -> None:
        self.game_id = game_id
        self.message = f"Game {game_id} not found"
        super().__init__(self.message)


class GameFullError(Exception):
    def __init__(self) -> None:
        self.message = "Game is full"
        super().__init__(self.message)


class CannotMoveError(Exception):
    def __init__(self, status: str) -> None:
        self.status = status
        self.message = f"Cannot make move. Game status: {status}"
        super().__init__(self.message)


class PlayerNotInGameError(Exception):
    def __init__(self) -> None:
        self.message = "Player not in this game"
        super().__init__(self.message)


class NotYourTurnError(Exception):
    def __init__(self, current_player: str) -> None:
        self.current_player = current_player
        self.message = f"Not your turn. Current player: {self.current_player}"
        super().__init__(self.message)


class InvalidPositionError(Exception):
    def __init__(self) -> None:
        self.message = "Position must be between 0-2 for both row and col"
        super().__init__(self.message)


class PositionOccupiedError(Exception):
    def __init__(self) -> None:
        self.message = "Position already occupied"
        super().__init__(self.message)
