from players.models import Player

CAPACITY = 2


class Room:
    def __init__(self, room_id: str) -> None:
        self.id = room_id
        self.players: list[Player] = []
        self.active_player: Player

    def is_open(self) -> bool:
        return len(self.players) < CAPACITY

    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def remove_player(self, client_id: int) -> None:
        self.players = [p for p in self.players if p.id != client_id]
