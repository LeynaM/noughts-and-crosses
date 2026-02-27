from enum import Enum

from board.models import Board
from players.models import Player

CAPACITY = 2


class GameStatus(str, Enum):
    PLAYING = "PLAYING"
    WAITING_FOR_OPPONENT = "WAITING_FOR_OPPONENT"


class Room:
    def __init__(self, room_id: str) -> None:
        self.id = room_id
        self.players: list[Player] = []
        self.active_player: Player
        self.board = Board()
        self.status = GameStatus.WAITING_FOR_OPPONENT
        self.winner = None

    def is_open(self) -> bool:
        return len(self.players) < CAPACITY

    def add_player(self, player: Player) -> None:
        if not self.is_open():
            return

        self.active_player = player
        self.players.append(player)
        if not self.is_open():
            self.status = GameStatus.PLAYING

    def remove_player(self, client_id: int) -> None:
        self.players = [p for p in self.players if p.id != client_id]

        if self.isOpen():
            self.status = GameStatus.WAITING_FOR_OPPONENT
