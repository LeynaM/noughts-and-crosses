from domain.value_objects.enums import PlayerSymbol
from domain.value_objects.position import Position
from errors import PositionOccupiedError


class Board:
    def __init__(self) -> None:
        self._grid: list[list[PlayerSymbol | None]] = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def make_move(self, position: Position, symbol: PlayerSymbol) -> None:
        if self._grid[position.row][position.col] is not None:
            raise PositionOccupiedError
        self._grid[position.row][position.col] = symbol

    def get_cell(self, position: Position) -> PlayerSymbol | None:
        return self._grid[position.row][position.col]

    def is_position_empty(self, position: Position) -> bool:
        return self._grid[position.row][position.col] is None

    def is_full(self) -> bool:
        return all(cell is not None for row in self._grid for cell in row)

    def get_grid(self) -> list[list[str | None]]:
        return [[cell.value if cell else None for cell in row] for row in self._grid]

    def from_grid(self, grid: list[list[str | None]]) -> None:
        self._grid = [[PlayerSymbol(cell) if cell else None for cell in row] for row in grid]

    def check_winner(self) -> PlayerSymbol | None:
        for row in self._grid:
            if row[0] and row[0] == row[1] == row[2]:
                return row[0]

        for col in range(3):
            if (
                self._grid[0][col]
                and self._grid[0][col] == self._grid[1][col] == self._grid[2][col]
            ):
                return self._grid[0][col]

        if (
            self._grid[0][0]
            and self._grid[0][0] == self._grid[1][1] == self._grid[2][2]
        ):
            return self._grid[0][0]

        if (
            self._grid[0][2]
            and self._grid[0][2] == self._grid[1][1] == self._grid[2][0]
        ):
            return self._grid[0][2]

        return None
