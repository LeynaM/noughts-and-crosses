from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas import CreateGameResponse, ErrorResponse, GameResponse
from dependencies import get_game_service
from services.game_service import GameService

router = APIRouter(prefix="/games", tags=["games"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new game",
    description="Creates a new game and waits for players to connect via WebSocket",
)
async def create_game(
    service: Annotated[GameService, Depends(get_game_service)] = None,
) -> CreateGameResponse:
    game = await service.create_game()
    return CreateGameResponse(
        id=game.id,
    )


@router.get(
    "/{game_id}",
    summary="Get game by ID",
    description="Retrieves the current state of a game",
    responses={404: {"model": ErrorResponse, "description": "Game not found"}},
)
async def get_game(
    game_id: UUID, service: Annotated[GameService, Depends(get_game_service)]
) -> GameResponse:
    game = await service.get_game(game_id)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Game {game_id} not found"
        )

    game_dict = game.to_dict()
    return GameResponse(**game_dict)


@router.get(
    "",
    summary="List all games",
    description="Retrieves a list of all games",
)
async def list_games(
    service: Annotated[GameService, Depends(get_game_service)],
) -> list[GameResponse]:
    """List all games."""
    games = await service.list_games()
    return [GameResponse(**game.to_dict()) for game in games]


@router.delete(
    "/{game_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a game",
    description="Deletes a game by ID",
    responses={404: {"model": ErrorResponse, "description": "Game not found"}},
)
async def delete_game(
    game_id: UUID, service: Annotated[GameService, Depends(get_game_service)]
) -> None:
    deleted = await service.delete_game(game_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Game {game_id} not found"
        )
