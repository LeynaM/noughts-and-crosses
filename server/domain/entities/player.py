class PlayerInfo:
    def __init__(self, username: str) -> None:
        self.username = username
        self.connected = True

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "connected": self.connected,
        }
