from .models import Usuario, Room, Reserva
from .storage import UsuarioStorage, RoomStorage, ReservaStorage
from .exceptions import RoomNoDisponibleError, RoomNoEncontradaError, UsuarioNoEncontradoError, ReservaNoEncontradaError, DatosInvalidosError


class UsuarioService:

    def __init__(self, storage: UsuarioStorage) -> None:
        self._storage = storage

    """Ejemplo de Docstring

    Args:
        user: User instance containging the data to be stored
    
    Raises:
        UserAlreadyExistsError: If a user with the same ID
        already exists.
        InvalidUserDataError: If the user data is invalid.
    """

    def listar(self) -> list[Usuario]:
        return self._storage.obtener_todos()

    def buscar(self, id_user: int) -> Usuario:
        for u in self._storage.obtener_todos():
            if u.id_user == id_user:
                return u
        raise UsuarioNoEncontradoError(f"Usuario {id_user} no existe")

    def registrar(self, usuario: Usuario) -> None:
        if "@" not in usuario.email:
            raise DatosInvalidosError("Email invalido")
        if not usuario.telefono.strip():
            raise DatosInvalidosError("Telefono vacio")
        self._storage.guardar(usuario)


class RoomService:
    
    def __init__(self, storage: RoomStorage) -> None:
        self._storage = storage

    def listar(self) -> list[Room]:
        return self._storage.obtener_todas()

    def listar_disponibles(self) -> list[Room]:
        return [r for r in self._storage.obtener_todas() if r.reservada_por is None]

    def buscar(self, id_room: int) -> Room:
        for r in self._storage.obtener_todas():
            if r.id == id_room:
                return r
        raise RoomNoEncontradaError(f"Habitacion {id_room} no existe")


class ReservaService:

    def __init__(self, storage: ReservaStorage, rooms: RoomService, usuarios: UsuarioService) -> None:
        self._storage = storage
        self._rooms = rooms
        self._usuarios = usuarios

    def crear(self, id_usuario: int, id_room: int, horas: int) -> Reserva:
        if horas <= 0:
            raise DatosInvalidosError("Las horas deben ser mayor a 0")
        usuario = self._usuarios.buscar(id_usuario)
        room = self._rooms.buscar(id_room)
        if room.reservada_por is not None:
            raise RoomNoDisponibleError(f"La habitacion {id_room} ya esta reservada")
        reservas = self._storage.obtener_todas()
        nuevo_id = max((r.id for r in reservas), default=0) + 1
        reserva = Reserva(id=nuevo_id, id_usuario=usuario.id_user, id_room=room.id, horas=horas, total=room.precio * horas)
        room.reservada_por = usuario.id_user
        self._rooms._storage.guardar(room)
        self._storage.guardar(reserva)
        return reserva

    def cancelar(self, reserva_id: int) -> None:
        for reserva in self._storage.obtener_todas():
            if reserva.id == reserva_id:
                if reserva.estado != "activa":
                    raise DatosInvalidosError("Solo se cancelan reservas activas")
                reserva.estado = "cancelada"
                room = self._rooms.buscar(reserva.id_room)
                room.reservada_por = None
                self._rooms._storage.guardar(room)
                self._storage.guardar(reserva)
                return
        raise ReservaNoEncontradaError(f"Reserva {reserva_id} no existe")

    def listar(self) -> list[Reserva]:
        return self._storage.obtener_todas()