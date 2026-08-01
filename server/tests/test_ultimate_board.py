import pytest

from domain.entities.ultimate_board import UltimateBoard
from domain.value_objects.enums import PlayerSymbol
from domain.value_objects.position import Position, UltimatePosition
from errors import BoardDecidedError, PositionOccupiedError, WrongBoardError

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


def play(  # noqa: PLR0913
    board: UltimateBoard,
    board_row: int,
    board_col: int,
    row: int,
    col: int,
    symbol: PlayerSymbol = CROSS,
) -> None:
    board.make_move(
        UltimatePosition(Position(board_row, board_col), Position(row, col)), symbol
    )


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


def test_first_move_can_go_anywhere() -> None:
    board = UltimateBoard()
    assert board.active_board is None

    play(board, 2, 2, 0, 1)

    assert board.active_board == (0, 1)


def test_move_outside_the_active_board_is_rejected() -> None:
    board = UltimateBoard()
    play(board, 2, 2, 0, 1)

    with pytest.raises(WrongBoardError):
        play(board, 1, 1, 0, 0, NOUGHT)


def test_occupied_cell_is_rejected() -> None:
    board = UltimateBoard()
    play(board, 1, 1, 1, 1)

    with pytest.raises(PositionOccupiedError):
        play(board, 1, 1, 1, 1, NOUGHT)


def test_winning_a_small_board_claims_the_large_cell() -> None:
    board = UltimateBoard()
    fill(board, 0, 0, win_for(CROSS))

    assert board.get_meta_grid()[0][0] == "X"
    assert board.is_decided((0, 0))


def test_being_sent_to_the_board_just_won_frees_the_next_player() -> None:
    board = UltimateBoard()
    play(board, 0, 0, 0, 2)
    play(board, 0, 2, 0, 0, NOUGHT)
    play(board, 0, 0, 0, 1)
    play(board, 0, 1, 0, 0, NOUGHT)
    # Completes row 0 of board (0, 0), and points at board (0, 0).
    play(board, 0, 0, 0, 0)

    assert board.get_meta_grid()[0][0] == "X"
    assert board.active_board is None


def test_drawn_board_claims_nothing_and_leaves_play() -> None:
    board = UltimateBoard()
    fill(board, 1, 1, DRAW)

    assert board.get_meta_grid()[1][1] is None
    assert board.get_drawn() == [[1, 1]]
    assert board.is_decided((1, 1))

    board.active_board = None
    with pytest.raises(BoardDecidedError):
        play(board, 1, 1, 0, 0)


def test_three_claimed_cells_in_a_line_wins() -> None:
    board = UltimateBoard()
    for col in range(3):
        fill(board, 0, col, win_for(CROSS))

    assert board.check_winner() is CROSS


def test_is_full_only_once_every_board_is_decided() -> None:
    board = UltimateBoard()
    keys = [(row, col) for row in range(3) for col in range(3)]

    for row, col in keys[:-1]:
        fill(board, row, col, DRAW)
    assert not board.is_full()

    fill(board, *keys[-1], DRAW)
    assert board.is_full()
    assert board.check_winner() is None


def test_reset_clears_the_boards_claims_and_target() -> None:
    board = UltimateBoard()
    fill(board, 0, 0, win_for(CROSS))
    fill(board, 1, 1, DRAW)

    board.reset()

    assert board.active_board is None
    assert board.get_drawn() == []
    assert board.check_winner() is None
    assert board.get_meta_grid() == [[None] * 3 for _ in range(3)]
    assert board.get_grid()[0][0] == [[None] * 3 for _ in range(3)]
