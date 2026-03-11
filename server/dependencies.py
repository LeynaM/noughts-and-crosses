from domain.repositories import GameRepository
from infrastructure.repositories import InMemoryGameRepository
from infrastructure.websocket_manager import ConnectionManager
from services.game_service import GameService

_repository: GameRepository = InMemoryGameRepository()
_connection_manager: ConnectionManager = ConnectionManager()
_game_service: GameService = GameService(_repository, _connection_manager)


def get_game_repository() -> GameRepository:
    return _repository


def get_connection_manager() -> ConnectionManager:
    return _connection_manager


def get_game_service() -> GameService:
    return _game_service
