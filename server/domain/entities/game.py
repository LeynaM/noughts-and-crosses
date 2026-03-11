from datetime import UTC, datetime
from uuid import UUID, uuid4

from domain.entities.board import Board
from domain.entities.player import PlayerInfo
from domain.value_objects.enums import GameStatus, Player
from domain.value_objects.position import Position
from errors import (
    CannotMoveError,
    GameFullError,
    NotYourTurnError,
    PlayerNotInGameError,
)


class Game:
    def __init__(self, game_id: UUID | None = None) -> None:
        self.id: UUID = game_id or uuid4()
        self.board: Board = Board()
        self.current_player: Player = Player.X
        self.status: GameStatus = GameStatus.WAITING_FOR_OPPONENT
        self.winner: Player | None = None

        self.player_x: PlayerInfo | None = None
        self.player_o: PlayerInfo | None = None

        self.created_at: datetime = datetime.now(UTC)
        self.updated_at: datetime = datetime.now(UTC)
        self.started_at: datetime | None = None
        self.ended_at: datetime | None = None

    def add_player(self, username: str | None) -> Player:
        if not self.player_x:
            self.player_x = PlayerInfo(username)
            return Player.X
        if not self.player_o:
            self.player_o = PlayerInfo(username)
            self.status = GameStatus.IN_PROGRESS
            self.started_at = datetime.now(UTC)
            return Player.O
        raise GameFullError

    def get_player_role(self, username: str) -> Player | None:
        if self.player_x and self.player_x.username == username:
            return Player.X
        if self.player_o and self.player_o.username == username:
            return Player.O
        return None

    def is_player_in_game(self, username: str) -> bool:
        return self.get_player_role(username) is not None

    def is_full(self) -> bool:
        return self.player_x is not None and self.player_o is not None

    def make_move(self, username: str, position: Position) -> None:
        if self.status not in [GameStatus.IN_PROGRESS]:
            raise CannotMoveError(self.status.value)

        player_role = self.get_player_role(username)
        if not player_role:
            raise PlayerNotInGameError

        if player_role != self.current_player:
            raise NotYourTurnError(self.current_player.value)

        self.board.make_move(position, self.current_player)
        self._update_game_state()

        if self.status == GameStatus.IN_PROGRESS:
            self._switch_player()

        self.updated_at = datetime.now(UTC)

    def handle_player_disconnect(self, username: str) -> None:
        if self.player_x and self.player_x.username == username:
            self.player_x.connected = False
        elif self.player_o and self.player_o.username == username:
            self.player_o.connected = False

        if self.status == GameStatus.IN_PROGRESS:
            self.status = GameStatus.ABANDONED
            self.ended_at = datetime.now(UTC)

    def handle_player_reconnect(self, username: str) -> None:
        if self.player_x and self.player_x.username == username:
            self.player_x.connected = True
        elif self.player_o and self.player_o.username == username:
            self.player_o.connected = True

    def _switch_player(self) -> None:
        self.current_player = Player.O if self.current_player == Player.X else Player.X

    def _update_game_state(self) -> None:
        winner = self.board.check_winner()

        if winner:
            self.winner = winner
            self.status = (
                GameStatus.PLAYER_X_WON
                if winner == Player.X
                else GameStatus.PLAYER_O_WON
            )
            self.ended_at = datetime.now(UTC)
        elif self.board.is_full():
            self.status = GameStatus.DRAW
            self.ended_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "board": self.board.get_grid(),
            "current_player": self.current_player.value,
            "status": self.status.value,
            "winner": self.winner.value if self.winner else None,
            "player_x": self.player_x.to_dict() if self.player_x else None,
            "player_o": self.player_o.to_dict() if self.player_o else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
        }
