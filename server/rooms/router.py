from typing import Annotated

from fastapi import APIRouter, Depends, status

from dependencies import get_room_repository
from repository.models import RoomRepository
from rooms.models import Room
from utils.generate_id import generate_id

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_room(
    room_repository: Annotated[RoomRepository, Depends(get_room_repository)],
) -> str:
    room_id = generate_id()
    new_room = Room(room_id)
    room_repository.add(new_room)
    return room_id
