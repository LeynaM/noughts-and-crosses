from errors import InvalidPositionError


class Position:
    def __init__(self, row: int, col: int) -> None:
        if not (0 <= row < 3 and 0 <= col < 3):  # noqa: PLR2004
            raise InvalidPositionError
        self.row = row
        self.col = col

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            return False
        return self.row == other.row and self.col == other.col

    def __hash__(self) -> int:
        return hash((self.row, self.col))

    def __repr__(self) -> str:
        return f"Position(row={self.row}, col={self.col})"
