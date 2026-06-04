"""
FastAPI router for Reservation endpoints.
"""

from fastapi import APIRouter, HTTPException, status
from src.storage.base import get_supabase_client
from src.storage.reservation_repository import ReservationRepository
from src.storage.room_repository import RoomRepository
from src.storage.user_repository import UserRepository
from src.services.reservation_service import ReservaService
from src.services.room_service import RoomService
from src.services.user_service import UsuarioService
from src.schemas.reserva import ReservaCreate, ReservaResponse
from src.core.exceptions import MotelError

router = APIRouter(prefix="/reservas", tags=["Reservations"])


def _get_service() -> ReservaService:
    client = get_supabase_client()
    
    # Instanciar repositorios y servicios dependientes
    user_repo = UserRepository(client)
    user_service = UsuarioService(user_repo)
    
    room_repo = RoomRepository(client)
    room_service = RoomService(room_repo)
    
    res_repo = ReservationRepository(client)
    return ReservaService(res_repo, room_service, user_service)


@router.get("/", response_model=list[ReservaResponse])
def listar_reservas():
    service = _get_service()
    return service.listar()


@router.post("/", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
def crear_reserva(command: ReservaCreate):
    service = _get_service()
    try:
        return service.crear(command)
    except MotelError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{reserva_id}/cancelar", response_model=ReservaResponse)
def cancelar_reserva(reserva_id: int):
    service = _get_service()
    try:
        return service.cancelar(reserva_id)
    except MotelError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))