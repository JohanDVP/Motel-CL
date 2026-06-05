"""Router de FastAPI para los endpoints de Habitaciones."""

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_room_service
from src.core.exceptions import MotelError, RoomNoEncontradaError
from src.schemas.room import RoomCreate, RoomResponse
from src.services.room_service import RoomService

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=list[RoomResponse])
def listar_habitaciones(
    disponibles_only: bool = False,
    service: RoomService = Depends(get_room_service),
):
    """Obtiene las habitaciones, filtrando opcionalmente por disponibilidad.

    Args:
        disponibles_only (bool): Si es True, solo lista habitaciones libres.

    Returns:
        list[RoomResponse]: Lista de habitaciones según el filtro.
    """
    if disponibles_only:
        return service.listar_disponibles()
    return service.listar()


@router.get("/{id_room}", response_model=RoomResponse)
def buscar_habitacion(id_room: int, service: RoomService = Depends(get_room_service)):
    """Obtiene información detallada de una habitación específica.

    Args:
        id_room (int): El ID de la habitación.

    Raises:
        HTTPException: Si la habitación no se encuentra (404).

    Returns:
        RoomResponse: Información de la habitación.
    """
    try:
        return service.buscar(id_room)
    except RoomNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def crear_habitacion(
    room: RoomCreate, service: RoomService = Depends(get_room_service)
):
    """Registra una nueva habitación en el sistema.

    Args:
        room (RoomCreate): Datos para la nueva habitación.

    Raises:
        HTTPException: Si los datos son inválidos (400).

    Returns:
        RoomResponse: La habitación recién creada.
    """
    try:
        return service.crear(room)
    except MotelError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.put("/{id_room}", response_model=RoomResponse)
def actualizar_habitacion(
    id_room: int,
    room: RoomCreate,
    service: RoomService = Depends(get_room_service),
):
    """Actualiza características técnicas o precios de una habitación.

    Args:
        id_room (int): El ID de la habitación a actualizar.
        room (RoomCreate): Nuevos datos de la habitación.

    Raises:
        HTTPException: Si la habitación no se encuentra (404) o es inválida (400).

    Returns:
        RoomResponse: El objeto de la habitación actualizado.
    """
    try:
        return service.actualizar(id_room, room)
    except RoomNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except MotelError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.delete("/{id_room}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_habitacion(id_room: int, service: RoomService = Depends(get_room_service)):
    """Elimina el registro de una habitación del sistema.

    Args:
        id_room (int): El ID de la habitación a eliminar.

    Raises:
        HTTPException: Si no se encuentra (404) o no se puede eliminar (400).
    """
    try:
        service.eliminar(id_room)
    except RoomNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except MotelError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e