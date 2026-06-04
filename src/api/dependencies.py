"""
Authentication and Service Dependency Injection providers.
"""

from src.services.reservation_service import ReservaService
from src.services.room_service import RoomService
from src.services.user_service import UsuarioService
from src.storage.base import get_supabase_client
from src.storage.reservation_repository import ReservationRepository
from src.storage.room_repository import RoomRepository
from src.storage.user_repository import UserRepository


def get_user_service() -> UsuarioService:
    client = get_supabase_client()
    repo = UserRepository(client)
    return UsuarioService(repo)


def get_room_service() -> RoomService:
    client = get_supabase_client()
    repo = RoomRepository(client)
    return RoomService(repo)


def get_reserva_service() -> ReservaService:
    client = get_supabase_client()

    # Inyectamos los servicios hermanos para mantener el desacoplamiento
    user_service = get_user_service()
    room_service = get_room_service()
    res_repo = ReservationRepository(client)

    return ReservaService(res_repo, room_service, user_service)
