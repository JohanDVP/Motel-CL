"""Capa de servicios del sistema Motel."""

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
    """Gestiona las operaciones sobre usuarios del motel."""

    def __init__(self, storage: UsuarioStorage) -> None:
        self._storage = storage

    def listar(self) -> list[Usuario]:
        """Retorna todos los usuarios registrados."""
        return self._storage.obtener_todos()

    def buscar(self, id_user: int) -> Usuario:
        """Busca un usuario por ID."""
        usuario = next(
            (u for u in self._storage.obtener_todos() if u.id_user == id_user),
            None,
        )
        if usuario is None:
            raise UsuarioNoEncontradoError(f"Usuario {id_user} no existe")
        return usuario

    def registrar(self, usuario: Usuario) -> None:
        """Registra un nuevo usuario."""
        self._validar_email(usuario.email)
        self._validar_telefono(usuario.telefono)
        self._storage.guardar(usuario)

    def _validar_email(self, email: str) -> None:
        if "@" not in email:
            raise DatosInvalidosError("Email inválido")

    def _validar_telefono(self, telefono: str) -> None:
        if not telefono.strip():
            raise DatosInvalidosError("Teléfono vacío")


# --------------------------------------------


class RoomService:
    """Gestiona las operaciones sobre habitaciones del motel."""

    def __init__(self, storage: RoomStorage) -> None:
        self._storage = storage

    def listar(self) -> list[Room]:
        """Retorna todas las habitaciones."""
        return self._storage.obtener_todas()

    def listar_disponibles(self) -> list[Room]:
        """Retorna solo las habitaciones disponibles."""
        return [
            r for r in self._storage.obtener_todas()
            if r.reservada_por is None
        ]

    def buscar(self, id_room: int) -> Room:
        """Busca una habitación por ID."""
        room = next(
            (r for r in self._storage.obtener_todas() if r.id == id_room),
            None,
        )
        if room is None:
            raise RoomNoEncontradaError(f"Habitación {id_room} no existe")
        return room

    def actualizar(self, room: Room) -> None:
        """Guarda cambios en una habitación."""
        self._storage.guardar(room)


# --------------------------------------------


class ReservaService:
    """Gestiona el ciclo de vida de las reservas."""

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
        """Retorna todas las reservas."""
        return self._storage.obtener_todas()

    def crear(self, id_usuario: int, id_room: int, horas: int) -> Reserva:
        """Crea una nueva reserva."""

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
        """Cancela una reserva activa."""

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
        if horas <= 0:
            raise DatosInvalidosError("Las horas deben ser mayor a 0")

    def _validar_disponibilidad(self, room: Room) -> None:
        if room.reservada_por is not None:
            raise RoomNoDisponibleError(
                f"La habitación {room.id} ya está reservada"
            )

    def _crear_reserva(self, usuario: Usuario, room: Room, horas: int) -> Reserva:
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
        reserva = next(
            (r for r in self._storage.obtener_todas() if r.id == reserva_id),
            None,
        )
        if reserva is None:
            raise ReservaNoEncontradaError(
                f"Reserva {reserva_id} no existe"
            )
        return reserva