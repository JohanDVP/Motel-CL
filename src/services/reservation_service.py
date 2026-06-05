"""Servicio de lógica de negocio que maneja el ciclo de vida de las 
reservas del motel."""

from src.core.exceptions import (
    DatosInvalidosError,
    ReservaNoEncontradaError,
    RoomNoDisponibleError,
)
from src.schemas.reserva import ReservaCreate, ReservaResponse
from src.services.room_service import RoomService
from src.services.user_service import UsuarioService
from src.storage.reservation_repository import ReservationRepository


class ReservaService:
    """Clase de servicio para gestionar las operaciones de negocio de reservas del
    motel."""

    def __init__(
        self,
        repository: ReservationRepository,
        room_service: RoomService,
        user_service: UsuarioService,
    ) -> None:
        """Inicializa el servicio de reservas con las dependencias requeridas."""
        self._repository = repository
        self._room_service = room_service
        self._user_service = user_service

    def listar(self) -> list[ReservaResponse]:
        """Recupera el historial completo de reservas desde el repositorio.

        Returns:
            list[ReservaResponse]: Una lista de todas las reservas registradas.
        """
        return self._repository.get_all()

    def buscar(self, reserva_id: int) -> ReservaResponse:
        """Busca una reserva por su ID.

        Args:
            reserva_id (int): El identificador único de la reserva.

        Returns:
            ReservaResponse: El objeto de la reserva encontrada.

        Raises:
            ReservaNoEncontradaError: Si no existe una reserva con el ID
                proporcionado.
        """
        reserva = self._repository.get_by_id(reserva_id)
        if reserva is None:
            raise ReservaNoEncontradaError(f"La reserva {reserva_id} no existe.")
        return reserva

    def crear(self, command: ReservaCreate) -> ReservaResponse:
        """Crea una nueva reserva, actualiza la ocupación de la habitación y
        persiste los datos.

        Args:
            command (ReservaCreate): Datos que contienen el ID de usuario,
                ID de habitación y horas.

        Returns:
            ReservaResponse: La reserva recién creada.

        Raises:
            RoomNoDisponibleError: Si la habitación solicitada ya está ocupada.
        """
        usuario = self._user_service.buscar(command.id_usuario)
        room = self._room_service.buscar(command.id_room)

        if room.reservada_por is not None:
            raise RoomNoDisponibleError(
                f"La habitación {room.id} ya está reservada."
            )

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
        """Cancela una reserva activa y libera completamente la habitación.

        Args:
            reserva_id (int): El ID de la reserva a cancelar.

        Returns:
            ReservaResponse: El objeto de la reserva actualizada.

        Raises:
            DatosInvalidosError: Si la reserva no está en estado 'activa'.
        """
        reserva = self.buscar(reserva_id)

        if reserva.estado != "activa":
            raise DatosInvalidosError(
                "Solo se pueden cancelar reservas en estado 'activa'."
            )

        reserva_actualizada = self._repository.update_status(reserva_id, "cancelada")
        self._room_service.liberar_habitacion(reserva.id_room)
        return reserva_actualizada

    def actualizar(self, reserva_id: int, command: ReservaCreate) -> ReservaResponse:
        """Actualiza los detalles de la reserva y recalcula el precio final.

        Args:
            reserva_id (int): El ID de la reserva a actualizar.
            command (ReservaCreate): Nuevos datos para la reserva.

        Returns:
            ReservaResponse: El objeto de la reserva actualizada.
        """
        self.buscar(reserva_id)

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

    def eliminar(self, reserva_id: int) -> None:
        """Elimina un registro de reserva y libera de forma segura su habitación
        asociada.

        Args:
            reserva_id (int): El ID de la reserva a eliminar.
        """
        reserva = self.buscar(reserva_id)
        if reserva.estado == "activa":
            self._room_service.liberar_habitacion(reserva.id_room)
        self._repository.delete(reserva_id)