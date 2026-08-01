import pytest
from helpers import CROSS, at, fill, win_for

from domain.entities.board import Board
from domain.entities.game import Game
from domain.entities.ultimate_board import UltimateBoard
from domain.value_objects.enums import GameMode, GameStatus, PlayerSymbol
from domain.value_objects.position import Position
from errors import InvalidPositionError

EMPTY = [[None] * 3 for _ in range(3)]


def started(mode: GameMode) -> Game:
    game = Game(mode=mode)
    game.add_player("alice")
    game.add_player("bob")
    return game


def test_classic_is_the_default() -> None:
    game = Game()

    assert game.mode is GameMode.CLASSIC
    assert isinstance(game.board, Board)

    data = game.to_dict()
    assert data["mode"] == "classic"
    assert data["board"] == EMPTY
    assert "meta_board" not in data


def test_ultimate_game_holds_a_nested_board() -> None:
    game = Game(mode=GameMode.ULTIMATE)

    assert isinstance(game.board, UltimateBoard)

    data = game.to_dict()
    assert data["mode"] == "ultimate"
    assert data["board"][0][0] == EMPTY
    assert data["meta_board"] == EMPTY
    assert data["drawn_boards"] == []
    assert data["active_board"] is None


def test_classic_play_is_unchanged() -> None:
    game = started(GameMode.CLASSIC)

    game.make_move("alice", Position(0, 0))

    assert game.current_player is PlayerSymbol.O
    assert game.to_dict()["board"][0][0] == "X"


def test_ultimate_move_switches_player_and_sets_the_target() -> None:
    game = started(GameMode.ULTIMATE)

    game.make_move("alice", at(2, 2, 0, 1))

    assert game.current_player is PlayerSymbol.O
    assert game.to_dict()["active_board"] == [0, 1]

    game.make_move("bob", at(0, 1, 1, 1))

    assert game.to_dict()["active_board"] == [1, 1]


def test_position_type_must_match_the_mode() -> None:
    classic = started(GameMode.CLASSIC)
    with pytest.raises(InvalidPositionError):
        classic.make_move("alice", at(0, 0, 0, 0))

    ultimate = started(GameMode.ULTIMATE)
    with pytest.raises(InvalidPositionError):
        ultimate.make_move("alice", Position(0, 0))


def test_claiming_three_boards_ends_the_ultimate_game() -> None:
    game = started(GameMode.ULTIMATE)
    board = game.board
    assert isinstance(board, UltimateBoard)

    fill(board, 0, 0, win_for(CROSS))
    fill(board, 0, 1, win_for(CROSS))
    # Two of X's three marks in board (0, 2), so alice's next move takes the row.
    for col in range(2):
        board.active_board = (0, 2)
        board.make_move(at(0, 2, 1, col), CROSS)

    board.active_board = (0, 2)
    game.make_move("alice", at(0, 2, 1, 2))

    assert game.status is GameStatus.OVER
    assert game.winner is PlayerSymbol.X


def test_rematch_keeps_the_mode_and_resets_the_board() -> None:
    game = started(GameMode.ULTIMATE)
    game.make_move("alice", at(1, 1, 2, 2))
    game.status = GameStatus.OVER

    game.rematch()

    assert game.mode is GameMode.ULTIMATE
    assert isinstance(game.board, UltimateBoard)
    assert game.board.active_board is None
    assert game.to_dict()["board"][1][1] == EMPTY
    assert game.to_dict()["player_x"] == {"username": "bob", "connected": True}
