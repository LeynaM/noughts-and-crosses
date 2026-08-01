from datetime import UTC, datetime
from uuid import UUID, uuid4

from domain.entities.board import Board
from domain.entities.player import Player
from domain.entities.ultimate_board import UltimateBoard
from domain.value_objects.enums import GameMode, GameStatus, PlayerSymbol
from domain.value_objects.position import Position, UltimatePosition
from errors import (
    CannotMoveError,
    CannotRematchError,
    GameFullError,
    InvalidPositionError,
    NotYourTurnError,
    PlayerNotInGameError,
)


class Game:
    def __init__(
        self, game_id: UUID | None = None, mode: GameMode = GameMode.CLASSIC
    ) -> None:
        self.id: UUID = game_id or uuid4()
        self.mode: GameMode = mode
        self.board: Board | UltimateBoard = (
            UltimateBoard() if mode is GameMode.ULTIMATE else Board()
        )
        self.current_player: PlayerSymbol = PlayerSymbol.X
        self.status: GameStatus = GameStatus.WAITING
        self.winner: PlayerSymbol | None = None
        self.player_x: Player | None = None
        self.player_o: Player | None = None
        self.players: dict[str, Player] = {}

        now = datetime.now(UTC)
        self.created_at: datetime = now
        self.updated_at: datetime = now
        self.started_at: datetime | None = None
        self.ended_at: datetime | None = None

    def add_player(self, username: str) -> Player:
        existing_players = list(self.players.values())
        if len(existing_players) >= 2:  # noqa: PLR2004
            raise GameFullError

        symbol = PlayerSymbol.X
        if len(existing_players) == 1:
            symbol = PlayerSymbol.O

        new_player = Player(username, symbol)
        self.players[username] = new_player

        if symbol == PlayerSymbol.X:
            self.player_x = new_player
        else:
            self.player_o = new_player

        self._update_game_status()
        return new_player

    def get_player_role(self, username: str) -> PlayerSymbol | None:
        player = self.players.get(username)
        if player:
            return player.symbol
        return None

    def is_player_in_game(self, username: str) -> bool:
        return username in self.players

    def is_full(self) -> bool:
        return self.player_x is not None and self.player_o is not None

    def make_move(self, username: str, position: Position | UltimatePosition) -> None:
        if self.status != GameStatus.IN_PROGRESS:
            raise CannotMoveError(self.status.value)

        player_role = self.get_player_role(username)
        if not player_role:
            raise PlayerNotInGameError

        if player_role != self.current_player:
            raise NotYourTurnError(self.current_player.value)

        self._place(position)
        self._update_game_status()

        if self.status == GameStatus.IN_PROGRESS:
            self._switch_player()

        self.updated_at = datetime.now(UTC)

    def rematch(self) -> None:
        if self.status != GameStatus.OVER:
            raise CannotRematchError(self.status.value)

        self.board.reset()
        self.winner = None
        self.current_player = PlayerSymbol.X

        # Whoever played O last time opens as X. Symbols live both on these
        # references and on the players themselves, so move them together.
        self.player_x, self.player_o = self.player_o, self.player_x
        if self.player_x:
            self.player_x.symbol = PlayerSymbol.X
        if self.player_o:
            self.player_o.symbol = PlayerSymbol.O

        self._update_game_status()
        self.updated_at = datetime.now(UTC)

    def reconnect_player(self, username: str) -> Player:
        self.players[username].connected = True
        self._update_game_status()
        return self.players[username]

    def disconnect_player(self, username: str) -> Player:
        self.players[username].connected = False
        self._update_game_status()
        return self.players[username]

    def _switch_player(self) -> None:
        self.current_player = (
            PlayerSymbol.O if self.current_player == PlayerSymbol.X else PlayerSymbol.X
        )

    def _place(self, position: Position | UltimatePosition) -> None:
        # Each mode's board only understands its own kind of position, and Game
        # is the one thing here that knows which mode it is.
        board = self.board
        if isinstance(board, UltimateBoard):
            if not isinstance(position, UltimatePosition):
                raise InvalidPositionError
            board.make_move(position, self.current_player)
            return

        if not isinstance(position, Position):
            raise InvalidPositionError
        board.make_move(position, self.current_player)

    def _update_game_status(self) -> None:
        previous = self.status

        winner = self.board.check_winner()
        if winner:
            self.winner = winner

        if winner or self.board.is_full():
            self.status = GameStatus.OVER
        else:
            has_disconnected = any(not p.connected for p in self.players.values())
            if len(self.players) == 2 and has_disconnected:  # noqa: PLR2004
                self.status = GameStatus.ABANDONED
            elif len(self.players) < 2:  # noqa: PLR2004
                self.status = GameStatus.WAITING
            else:
                self.status = GameStatus.IN_PROGRESS

        self._stamp_status_change(previous)

    def _stamp_status_change(self, previous: GameStatus) -> None:
        if self.status == previous:
            return

        ended = (GameStatus.OVER, GameStatus.ABANDONED)
        if self.status == GameStatus.IN_PROGRESS:
            # Also covers a rematch, which starts a fresh round in place.
            self.started_at = datetime.now(UTC)
            self.ended_at = None
        elif self.status in ended and previous not in ended:
            self.ended_at = datetime.now(UTC)

        self.updated_at = datetime.now(UTC)

    @staticmethod
    def _player_dict(player: Player | None) -> dict | None:
        if not player:
            return None
        return {"username": player.username, "connected": player.connected}

    def to_dict(self) -> dict:
        data: dict[str, object] = {
            "id": str(self.id),
            "mode": self.mode.value,
            "board": self.board.get_grid(),
            "current_player": self.current_player.value,
            "status": self.status.value,
            "winner": self.winner.value if self.winner else None,
            "player_x": self._player_dict(self.player_x),
            "player_o": self._player_dict(self.player_o),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
        }

        if isinstance(self.board, UltimateBoard):
            data["meta_board"] = self.board.get_meta_grid()
            data["drawn_boards"] = self.board.get_drawn()
            data["active_board"] = (
                list(self.board.active_board)
                if self.board.active_board is not None
                else None
            )

        return data
