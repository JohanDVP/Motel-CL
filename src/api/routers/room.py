"""
FastAPI router for Room endpoints.
"""

from fastapi import APIRouter, HTTPException, status
from src.storage.base import get_supabase_client
from src.storage.room_repository import RoomRepository
from src.services.room_service import RoomService
from src.schemas.room import RoomResponse
from src.core.exceptions import RoomNoEncontradaError

router = APIRouter(prefix="/rooms", tags=["Rooms"])


def _get_service() -> RoomService:
    client = get_supabase_client()
    repo = RoomRepository(client)
    return RoomService(repo)


@router.get("/", response_model=list[RoomResponse])
def listar_habitaciones(disponibles_only: bool = False):
    service = _get_service()
    if disponibles_only:
        return service.listar_disponibles()
    return service.listar()


@router.get("/{id_room}", response_model=RoomResponse)
def buscar_habitacion(id_room: int):
    service = _get_service()
    try:
        return service.buscar(id_room)
    except RoomNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))