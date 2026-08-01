from domain.entities.board import Board
from domain.value_objects.enums import PlayerSymbol
from domain.value_objects.position import Position, UltimatePosition
from errors import BoardDecidedError, InvalidPositionError, WrongBoardError

type BoardKey = tuple[int, int]


class UltimateBoard:
    def __init__(self) -> None:
        self._boards: list[list[Board]] = [
            [Board() for _ in range(3)] for _ in range(3)
        ]
        self._meta: Board = Board()
        # Decided, but claimed by nobody.
        self._drawn: set[BoardKey] = set()
        # None means the next move may go anywhere still in play.
        self.active_board: BoardKey | None = None

    def reset(self) -> None:
        self._boards = [[Board() for _ in range(3)] for _ in range(3)]
        self._meta = Board()
        self._drawn = set()
        self.active_board = None

    def make_move(self, position: UltimatePosition, symbol: PlayerSymbol) -> None:
        if not isinstance(position, UltimatePosition):
            raise InvalidPositionError

        target = (position.board.row, position.board.col)
        if self.active_board is not None and target != self.active_board:
            raise WrongBoardError(self.active_board)
        if self.is_decided(target):
            raise BoardDecidedError

        board = self._boards[target[0]][target[1]]
        board.make_move(position.cell, symbol)

        # Claim before choosing where to send them. Winning the board you are
        # about to point at is what frees the next player to play anywhere.
        winner = board.check_winner()
        if winner:
            self._meta.make_move(position.board, winner)
        elif board.is_full():
            self._drawn.add(target)

        destination = (position.cell.row, position.cell.col)
        self.active_board = None if self.is_decided(destination) else destination

    def is_decided(self, key: BoardKey) -> bool:
        return key in self._drawn or self._meta.get_cell(Position(*key)) is not None

    def check_winner(self) -> PlayerSymbol | None:
        return self._meta.check_winner()

    def is_full(self) -> bool:
        return all(self.is_decided((row, col)) for row in range(3) for col in range(3))

    def get_grid(self) -> list[list[list[list[str | None]]]]:
        return [[board.get_grid() for board in row] for row in self._boards]

    def get_meta_grid(self) -> list[list[str | None]]:
        return self._meta.get_grid()

    def get_drawn(self) -> list[list[int]]:
        return [[row, col] for row, col in sorted(self._drawn)]

    def to_payload(self) -> dict:
        # The extra state an ultimate game carries beyond the grid itself,
        # shared by the REST and WebSocket responses.
        return {
            "meta_board": self.get_meta_grid(),
            "drawn_boards": self.get_drawn(),
            "active_board": (
                list(self.active_board) if self.active_board is not None else None
            ),
        }
