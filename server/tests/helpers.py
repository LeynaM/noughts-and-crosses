from domain.entities.ultimate_board import UltimateBoard
from domain.value_objects.enums import PlayerSymbol
from domain.value_objects.position import Position, UltimatePosition

CROSS = PlayerSymbol.X
NOUGHT = PlayerSymbol.O

# Full, with no line. Ordered so the board only fills on the final cell.
DRAW: list[list[PlayerSymbol | None]] = [
    [CROSS, NOUGHT, CROSS],
    [CROSS, NOUGHT, NOUGHT],
    [NOUGHT, CROSS, CROSS],
]


def win_for(symbol: PlayerSymbol) -> list[list[PlayerSymbol | None]]:
    # The winning row is placed last, so the board is decided by the final cell.
    other = NOUGHT if symbol is CROSS else CROSS
    return [
        [other, other, None],
        [symbol, symbol, symbol],
        [None, None, None],
    ]


def at(board_row: int, board_col: int, row: int, col: int) -> UltimatePosition:
    return UltimatePosition(Position(board_row, board_col), Position(row, col))


def play(  # noqa: PLR0913
    board: UltimateBoard,
    board_row: int,
    board_col: int,
    row: int,
    col: int,
    symbol: PlayerSymbol = CROSS,
) -> None:
    board.make_move(at(board_row, board_col, row, col), symbol)


def fill(
    board: UltimateBoard,
    board_row: int,
    board_col: int,
    layout: list[list[PlayerSymbol | None]],
) -> None:
    # Arranges one small board, ignoring where each move would send the opponent.
    for row, cells in enumerate(layout):
        for col, symbol in enumerate(cells):
            if symbol is None:
                continue
            board.active_board = (board_row, board_col)
            play(board, board_row, board_col, row, col, symbol)
