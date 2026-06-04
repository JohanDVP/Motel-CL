"""
Business logic service handling the lifecycle of motel reservations.
"""

from src.storage.reservation_repository import ReservationRepository
from src.services.room_service import RoomService
from src.services.user_service import UsuarioService
from src.schemas.reserva import ReservaCreate, ReservaResponse
from src.core.exceptions import (
    ReservaNoEncontradaError,
    RoomNoDisponibleError,
    DatosInvalidosError,
)


class ReservaService:
    def __init__(
        self,
        repository: ReservationRepository,
        room_service: RoomService,
        user_service: UsuarioService,
    ) -> None:
        self._repository = repository
        self._room_service = room_service
        self._user_service = user_service

    def listar(self) -> list[ReservaResponse]:
        """Retrieves the complete reservation history."""
        return self._repository.get_all()

    def crear(self, command: ReservaCreate) -> ReservaResponse:
        """
        Creates a new reservation, updates room occupancy, and persists to Supabase.
        """
        # 1. Validar de forma estricta que existan tanto el usuario como la habitación
        usuario = self._user_service.buscar(command.id_usuario)
        room = self._room_service.buscar(command.id_room)

        # 2. Validar reglas de negocio: Disponibilidad de la habitación
        if room.reservada_por is not None:
            raise RoomNoDisponibleError(f"La habitación {room.id} ya se encuentra reservada.")

        # 3. Calcular el total financiero de forma segura en el servidor
        total_calculado = room.precio * command.horas

        # 4. Construir el payload exacto para la base de datos relacional
        payload = {
            "id_usuario": usuario.id_user,
            "id_room": room.id,
            "horas": command.horas,
            "total": total_calculado,
            "estado": "activa",
        }

        # 5. Guardar la reserva y marcar la habitación como ocupada en Supabase de forma atómica
        reserva_guardada = self._repository.create(payload)
        self._room_service._repository.update_reservation(room.id, usuario.id_user)

        return reserva_guardada

    def cancelar(self, reserva_id: int) -> ReservaResponse:
        """
        Cancels an active reservation and completely liberates the room.
        """
        reserva = self._repository.get_by_id(reserva_id)
        if reserva is None:
            raise ReservaNoEncontradaError(f"La reserva {reserva_id} no existe.")

        if reserva.estado != "activa":
            raise DatosInvalidosError("Únicamente se pueden cancelar reservaciones en estado 'activa'.")

        # 1. Cambiar estado de la reserva en Supabase
        reserva_actualizada = self._repository.update_status(reserva_id, "cancelada")
        
        # 2. Liberar la habitación (establecer reservada_por en NULL/None)
        self._room_service._repository.update_reservation(reserva.id_room, None)

        return reserva_actualizada