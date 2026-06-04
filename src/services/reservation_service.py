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

    # NUEVO: Método buscar para reutilizar en validaciones y exponer en API
    def buscar(self, reserva_id: int) -> ReservaResponse:
        """Finds a reservation by ID. Raises error if not found."""
        reserva = self._repository.get_by_id(reserva_id)
        if reserva is None:
            raise ReservaNoEncontradaError(f"La reserva con ID {reserva_id} no existe.")
        return reserva

    def crear(self, command: ReservaCreate) -> ReservaResponse:
        """Creates a new reservation, updates room occupancy, and persists to Supabase."""
        usuario = self._user_service.buscar(command.id_usuario)
        room = self._room_service.buscar(command.id_room)

        if room.reservada_por is not None:
            raise RoomNoDisponibleError(f"La habitación {room.id} ya se encuentra reservada.")

        total_calculado = room.precio * command.horas

        payload = {
            "id_usuario": usuario.id_user,
            "id_room": room.id,
            "horas": command.horas,
            "total": total_calculado,
            "estado": "activa",
        }

        reserva_guardada = self._repository.create(payload)
        self._room_service.marcar_como_ocupada(room.id, usuario.id_user)
        return reserva_guardada

    def cancelar(self, reserva_id: int) -> ReservaResponse:
        """Cancels an active reservation and completely liberates the room."""
        reserva = self.buscar(reserva_id)

        if reserva.estado != "activa":
            raise DatosInvalidosError("Únicamente se pueden cancelar reservaciones en estado 'activa'.")

        reserva_actualizada = self._repository.update_status(reserva_id, "cancelada")
        self._room_service.liberar_habitacion(reserva.id_room)
        return reserva_actualizada

    # NUEVO: Actualizar parámetros recalculando finanzas de manera limpia
    def actualizar(self, reserva_id: int, command: ReservaCreate) -> ReservaResponse:
        """Updates reservation details and recalculates the final pricing structure."""
        self.buscar(reserva_id)  # Valida que exista
        
        # Validamos que los nuevos datos de habitación y usuario sean reales
        self._user_service.buscar(command.id_usuario)
        room = self._room_service.buscar(command.id_room)
        
        total_calculado = room.precio * command.horas
        
        payload = {
            "id_usuario": command.id_usuario,
            "id_room": command.id_room,
            "horas": command.horas,
            "total": total_calculado,
        }
        return self._repository.update(reserva_id, payload)

    # NUEVO: Eliminar físicamente y liberar la habitación si estaba ocupada
    def eliminar(self, reserva_id: int) -> None:
        """Removes a reservation record and safely unlocks its associated room."""
        reserva = self.buscar(reserva_id)
        if reserva.estado == "activa":
            self._room_service.liberar_habitacion(reserva.id_room)
        self._repository.delete(reserva_id)