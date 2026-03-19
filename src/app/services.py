"""
Service layer for the Motel system.

Handles business logic for users, rooms, and reservations.
"""

from .models import Usuario, Room, Reserva
from .storage import UsuarioStorage, RoomStorage, ReservaStorage
from .exceptions import (
    RoomNoDisponibleError,
    RoomNoEncontradaError,
    UsuarioNoEncontradoError,
    ReservaNoEncontradaError,
    DatosInvalidosError,
)


class UsuarioService:
    """
    Handles business logic for motel users.

    Attributes:
        _storage (UsuarioStorage): Storage instance for user persistence.
    """

    def __init__(self, storage: UsuarioStorage) -> None:
        self._storage = storage

    def listar(self) -> list[Usuario]:
        """
        Retrieves all registered users.

        Returns:
            list[Usuario]: List of all users.
        """
        return self._storage.obtener_todos()

    def buscar(self, id_user: int) -> Usuario:
        """
        Finds a user by their ID.

        Args:
            id_user (int): The ID of the user to find.

        Returns:
            Usuario: The user found.

        Raises:
            UsuarioNoEncontradoError: If the user does not exist.
        """
        usuario = next(
            (u for u in self._storage.obtener_todos() if u.id_user == id_user),
            None,
        )
        if usuario is None:
            raise UsuarioNoEncontradoError(f"Usuario {id_user} no existe")
        return usuario

    def registrar(self, usuario: Usuario) -> None:
        """
        Registers a new user in the system.

        Args:
            usuario (Usuario): The user instance to register.

        Raises:
            DatosInvalidosError: If the email or phone number are invalid.
        """
        self._validar_email(usuario.email)
        self._validar_telefono(usuario.telefono)
        self._storage.guardar(usuario)

    def _validar_email(self, email: str) -> None:
        """
        Validates that the email contains '@'.

        Args:
            email (str): The email address to validate.

        Raises:
            DatosInvalidosError: If the email is invalid.
        """
        if "@" not in email:
            raise DatosInvalidosError("Email inválido")

    def _validar_telefono(self, telefono: str) -> None:
        """
        Validates that the phone number is not empty.

        Args:
            telefono (str): The phone number to validate.

        Raises:
            DatosInvalidosError: If the phone number is empty or blank.
        """
        if not telefono.strip():
            raise DatosInvalidosError("Teléfono vacío")


# --------------------------------------------


class RoomService:
    """
    Handles business logic for motel rooms.

    Attributes:
        _storage (RoomStorage): Storage instance for room persistence.
    """

    def __init__(self, storage: RoomStorage) -> None:
        self._storage = storage

    def listar(self) -> list[Room]:
        """
        Retrieves all rooms.

        Returns:
            list[Room]: List of all rooms.
        """
        return self._storage.obtener_todas()

    def listar_disponibles(self) -> list[Room]:
        """
        Retrieves only available rooms.

        Returns:
            list[Room]: List of rooms with no active reservation.
        """
        return [
            r for r in self._storage.obtener_todas()
            if r.reservada_por is None
        ]

    def buscar(self, id_room: int) -> Room:
        """
        Finds a room by its ID.

        Args:
            id_room (int): The ID of the room to find.

        Returns:
            Room: The room found.

        Raises:
            RoomNoEncontradaError: If the room does not exist.
        """
        room = next(
            (r for r in self._storage.obtener_todas() if r.id == id_room),
            None,
        )
        if room is None:
            raise RoomNoEncontradaError(f"Habitación {id_room} no existe")
        return room

    def actualizar(self, room: Room) -> None:
        """
        Saves changes to an existing room.

        Args:
            room (Room): The room instance with updated data.
        """
        self._storage.guardar(room)


# --------------------------------------------


class ReservaService:
    """
    Handles the lifecycle of motel reservations.

    Attributes:
        _storage (ReservaStorage): Storage instance for reservation persistence.
        _rooms (RoomService): Service for room operations.
        _usuarios (UsuarioService): Service for user operations.
    """

    def __init__(
        self,
        storage: ReservaStorage,
        rooms: RoomService,
        usuarios: UsuarioService,
    ) -> None:
        self._storage = storage
        self._rooms = rooms
        self._usuarios = usuarios

    def listar(self) -> list[Reserva]:
        """
        Retrieves all reservations.

        Returns:
            list[Reserva]: List of all reservations.
        """
        return self._storage.obtener_todas()

    def crear(self, id_usuario: int, id_room: int, horas: int) -> Reserva:
        """
        Creates a new reservation.

        Args:
            id_usuario (int): ID of the user making the reservation.
            id_room (int): ID of the room to reserve.
            horas (int): Duration of the reservation in hours.

        Returns:
            Reserva: The created reservation.

        Raises:
            DatosInvalidosError: If hours are zero or negative.
            UsuarioNoEncontradoError: If the user does not exist.
            RoomNoEncontradaError: If the room does not exist.
            RoomNoDisponibleError: If the room is already reserved.
        """
        self._validar_horas(horas)

        usuario = self._usuarios.buscar(id_usuario)
        room = self._rooms.buscar(id_room)

        self._validar_disponibilidad(room)

        reserva = self._crear_reserva(usuario, room, horas)

        room.reservada_por = usuario.id_user
        self._rooms.actualizar(room)
        self._storage.guardar(reserva)

        return reserva

    def cancelar(self, reserva_id: int) -> None:
        """
        Cancels an active reservation and releases the room.

        Args:
            reserva_id (int): ID of the reservation to cancel.

        Raises:
            ReservaNoEncontradaError: If the reservation does not exist.
            DatosInvalidosError: If the reservation is not active.
        """
        reserva = self._buscar_reserva(reserva_id)

        if reserva.estado != "activa":
            raise DatosInvalidosError("Solo se cancelan reservas activas")

        reserva.estado = "cancelada"

        room = self._rooms.buscar(reserva.id_room)
        room.reservada_por = None

        self._rooms.actualizar(room)
        self._storage.guardar(reserva)

    # -------------------------
    # MÉTODOS PRIVADOS
    # -------------------------

    def _validar_horas(self, horas: int) -> None:
        """
        Validates that hours are greater than zero.

        Args:
            horas (int): The number of hours to validate.

        Raises:
            DatosInvalidosError: If hours are zero or negative.
        """
        if horas <= 0:
            raise DatosInvalidosError("Las horas deben ser mayor a 0")

    def _validar_disponibilidad(self, room: Room) -> None:
        """
        Validates that a room is available for reservation.

        Args:
            room (Room): The room to check.

        Raises:
            RoomNoDisponibleError: If the room is already reserved.
        """
        if room.reservada_por is not None:
            raise RoomNoDisponibleError(
                f"La habitación {room.id} ya está reservada"
            )

    def _crear_reserva(self, usuario: Usuario, room: Room, horas: int) -> Reserva:
        """
        Builds a new Reserva instance with a generated ID.

        Args:
            usuario (Usuario): The user making the reservation.
            room (Room): The room being reserved.
            horas (int): Duration in hours.

        Returns:
            Reserva: The new reservation instance.
        """
        reservas = self._storage.obtener_todas()
        nuevo_id = max((r.id for r in reservas), default=0) + 1

        return Reserva(
            id=nuevo_id,
            id_usuario=usuario.id_user,
            id_room=room.id,
            horas=horas,
            total=room.precio * horas,
        )

    def _buscar_reserva(self, reserva_id: int) -> Reserva:
        """
        Finds a reservation by its ID.

        Args:
            reserva_id (int): The ID of the reservation to find.

        Returns:
            Reserva: The reservation found.

        Raises:
            ReservaNoEncontradaError: If the reservation does not exist.
        """
        reserva = next(
            (r for r in self._storage.obtener_todas() if r.id == reserva_id),
            None,
        )
        if reserva is None:
            raise ReservaNoEncontradaError(
                f"Reserva {reserva_id} no existe"
            )
        return reserva