class Board:
    def __init__(self) -> None:
        self.board: list[str] = []

    def place(self, content: str, coords: list[int]) -> None:
        pass

    def has_won(self, content: str, coords: list[int]) -> bool:
        pass

    def __repr__(self) -> None:
        return str(self.board)

    def __str__(self) -> None:
        return str(self.board)
