"""
FastAPI router for Reservation endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from src.services.reservation_service import ReservaService
from src.schemas.reserva import ReservaCreate, ReservaResponse
from src.core.exceptions import MotelError, ReservaNoEncontradaError
from src.api.dependencies import get_reserva_service

router = APIRouter(prefix="/reservas", tags=["Reservations"])


@router.get("/", response_model=list[ReservaResponse])
def listar_reservas(service: ReservaService = Depends(get_reserva_service)):
    """Endpoint to retrieve all reservations using dependency injection."""
    return service.listar()


# NUEVO: Endpoint para buscar una sola reserva por ID
@router.get("/{reserva_id}", response_model=ReservaResponse)
def buscar_reserva(reserva_id: int, service: ReservaService = Depends(get_reserva_service)):
    """Endpoint to fetch details of a specific reservation."""
    try:
        return service.buscar(reserva_id)
    except ReservaNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
def crear_reserva(
    command: ReservaCreate, 
    service: ReservaService = Depends(get_reserva_service)
):
    """Endpoint to create a new reservation."""
    try:
        return service.crear(command)
    except MotelError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{reserva_id}/cancelar", response_model=ReservaResponse)
def cancelar_reserva(
    reserva_id: int, 
    service: ReservaService = Depends(get_reserva_service)
):
    """Endpoint to safely cancel an active reservation."""
    try:
        return service.cancelar(reserva_id)
    except ReservaNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MotelError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# NUEVO: Endpoint para actualizar datos lógicos de la reserva
@router.put("/{reserva_id}", response_model=ReservaResponse)
def actualizar_reserva(
    reserva_id: int,
    command: ReservaCreate,
    service: ReservaService = Depends(get_reserva_service)
):
    """Endpoint to update scheduling details or rooms for an existing reservation."""
    try:
        return service.actualizar(reserva_id, command)
    except ReservaNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MotelError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# NUEVO: Endpoint para eliminación física
@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_reserva(reserva_id: int, service: ReservaService = Depends(get_reserva_service)):
    """Endpoint to purge a reservation logs from data schema."""
    try:
        service.eliminar(reserva_id)
    except ReservaNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MotelError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))