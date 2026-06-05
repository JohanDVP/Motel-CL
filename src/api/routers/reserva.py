"""Router de FastAPI para los endpoints de Reservas."""

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_reserva_service
from src.core.exceptions import MotelError, ReservaNoEncontradaError
from src.schemas.reserva import ReservaCreate, ReservaResponse
from src.services.reservation_service import ReservaService

router = APIRouter(prefix="/reservas", tags=["Reservations"])


@router.get("/", response_model=list[ReservaResponse])
def listar_reservas(service: ReservaService = Depends(get_reserva_service)):
    """Obtiene todas las reservas registradas en el sistema.

    Returns:
        list[ReservaResponse]: Una lista con todas las reservas activas y pasadas.
    """
    return service.listar()


@router.get("/{reserva_id}", response_model=ReservaResponse)
def buscar_reserva(
    reserva_id: int, service: ReservaService = Depends(get_reserva_service)
):
    """Busca los detalles de una reserva específica por su ID.

    Args:
        reserva_id (int): El identificador único de la reserva.

    Raises:
        HTTPException: Si la reserva no existe (404).

    Returns:
        ReservaResponse: Los detalles de la reserva solicitada.
    """
    try:
        return service.buscar(reserva_id)
    except ReservaNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.post("/", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
def crear_reserva(
    command: ReservaCreate, service: ReservaService = Depends(get_reserva_service)
):
    """Crea un nuevo registro de reserva.

    Args:
        command (ReservaCreate): Datos necesarios para crear la reserva.

    Raises:
        HTTPException: Si la habitación no está disponible o los
            datos son inválidos (400).

    Returns:
        ReservaResponse: El objeto de la reserva recién creada.
    """
    try:
        return service.crear(command)
    except MotelError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.post("/{reserva_id}/cancelar", response_model=ReservaResponse)
def cancelar_reserva(
    reserva_id: int, service: ReservaService = Depends(get_reserva_service)
):
    """Cancela de forma segura una reserva activa y libera la habitación.

    Args:
        reserva_id (int): El ID de la reserva a cancelar.

    Raises:
        HTTPException: Si la reserva no existe (404) o la operación falla (400).

    Returns:
        ReservaResponse: El objeto de la reserva actualizada.
    """
    try:
        return service.cancelar(reserva_id)
    except ReservaNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except MotelError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.put("/{reserva_id}", response_model=ReservaResponse)
def actualizar_reserva(
    reserva_id: int,
    command: ReservaCreate,
    service: ReservaService = Depends(get_reserva_service),
):
    """Actualiza los detalles de programación o habitaciones de una reserva existente.

    Args:
        reserva_id (int): El ID de la reserva a actualizar.
        command (ReservaCreate): Nuevos datos de la reserva.

    Raises:
        HTTPException: Si la reserva no existe (404) o los datos son inválidos (400).

    Returns:
        ReservaResponse: El objeto de la reserva actualizada.
    """
    try:
        return service.actualizar(reserva_id, command)
    except ReservaNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except MotelError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_reserva(
    reserva_id: int, service: ReservaService = Depends(get_reserva_service)
):
    """Elimina permanentemente un registro de reserva de la base de datos.

    Args:
        reserva_id (int): El ID de la reserva a eliminar.

    Raises:
        HTTPException: Si la reserva no existe (404) o no se puede eliminar (400).
    """
    try:
        service.eliminar(reserva_id)
    except ReservaNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except MotelError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e