"""
FastAPI router for Room endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from src.services.room_service import RoomService
from src.schemas.room import RoomCreate, RoomResponse
from src.core.exceptions import RoomNoEncontradaError, MotelError
from src.api.dependencies import get_room_service

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=list[RoomResponse])
def listar_habitaciones(
    disponibles_only: bool = False, 
    service: RoomService = Depends(get_room_service)
):
    """Retrieves rooms, optionally filtering by real-time availability."""
    if disponibles_only:
        return service.listar_disponibles()
    return service.listar()


@router.get("/{id_room}", response_model=RoomResponse)
def buscar_habitacion(id_room: int, service: RoomService = Depends(get_room_service)):
    """Retrieves detailed information of a specific room."""
    try:
        return service.buscar(id_room)
    except RoomNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def crear_habitacion(room: RoomCreate, service: RoomService = Depends(get_room_service)):
    """Registers a new room layout in the system."""
    try:
        return service.crear(room)
    except MotelError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_room}", response_model=RoomResponse)
def actualizar_habitacion(
    id_room: int,
    room: RoomCreate,
    service: RoomService = Depends(get_room_service)
):
    """Updates technical features or price details of a room."""
    try:
        return service.actualizar(id_room, room)
    except RoomNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MotelError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id_room}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_habitacion(id_room: int, service: RoomService = Depends(get_room_service)):
    """Deletes a room tracking index from the system data layer."""
    try:
        service.eliminar(id_room)
    except RoomNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MotelError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))