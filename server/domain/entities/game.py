from datetime import UTC, datetime
from uuid import UUID, uuid4

from domain.entities.board import Board
from domain.entities.player import Player
from domain.value_objects.enums import GameStatus, PlayerSymbol
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
        self.current_player: PlayerSymbol = PlayerSymbol.X
        self.status: GameStatus = GameStatus.WAITING_FOR_OPPONENT
        self.winner: PlayerSymbol | None = None
        self.player_x: Player | None = None
        self.player_o: Player | None = None
        self.players: dict[str, Player] = {}

    def add_player(self, username: str) -> Player:
        existing_players = list(self.players.values())
        if len(existing_players) >= 2:
            raise GameFullError

        symbol = PlayerSymbol.X
        if len(existing_players) == 1:
            symbol = PlayerSymbol.O
            self.status = GameStatus.IN_PROGRESS

        new_player = Player(username, symbol)
        self.players[username] = new_player
        return new_player

    def get_player_role(self, username: str) -> PlayerSymbol | None:
        if self.player_x and self.player_x.username == username:
            return PlayerSymbol.X
        if self.player_o and self.player_o.username == username:
            return PlayerSymbol.O
        return None

    def is_player_in_game(self, username: str) -> bool:
        return username in self.players

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

    def reconnect_player(self, username: str) -> Player:
        self.players[username].connected = True
        return self.players[username]

    def _switch_player(self) -> None:
        self.current_player = PlayerSymbol.O if self.current_player == PlayerSymbol.X else PlayerSymbol.X

    def _update_game_state(self) -> None:
        winner = self.board.check_winner()

        if winner:
            self.winner = winner
            self.status = (
                GameStatus.PLAYER_X_WON
                if winner == PlayerSymbol.X
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
        }
