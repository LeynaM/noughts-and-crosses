from domain.value_objects.enums import PlayerSymbol


class Player:
    def __init__(self, username: str, symbol: PlayerSymbol) -> None:
        self.username = username
        self.symbol = symbol
        self.connected = True
