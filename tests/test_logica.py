import pytest
from unittest.mock import MagicMock

from src.app.models import Usuario, Room, Reserva
from src.app.services import UsuarioService, RoomService, ReservaService
from src.app.exceptions import (
    RoomNoDisponibleError,
    RoomNoEncontradaError,
    UsuarioNoEncontradoError,
    DatosInvalidosError,
    ReservaNoEncontradaError,
)

# estos helpers crean servicios con datos falsos para no tocar el JSON real
def hacer_rooms(rooms: list[Room]) -> RoomService: 
    storage = MagicMock()
    storage.obtener_todas.return_value = rooms
    return RoomService(storage)


def hacer_usuarios(usuarios: list[Usuario]) -> UsuarioService:
    storage = MagicMock()
    storage.obtener_todos.return_value = usuarios
    return UsuarioService(storage)


def hacer_reservas(reservas: list[Reserva], rooms: list[Room], usuarios: list[Usuario]) -> ReservaService:
    storage = MagicMock()
    storage.obtener_todas.return_value = reservas
    return ReservaService(storage, hacer_rooms(rooms), hacer_usuarios(usuarios))


# pruebas de habitaciones

def test_solo_muestra_rooms_disponibles():
    rooms = [
        Room(id=1, tipo="Sencilla", precio=50.0, reservada_por=None),
        Room(id=2, tipo="Doble", precio=80.0, reservada_por=1),
    ]
    assert len(hacer_rooms(rooms).listar_disponibles()) == 1


def test_encuentra_room_por_id():
    rooms = [Room(id=3, tipo="Suite", precio=120.0)]
    assert hacer_rooms(rooms).buscar(3).tipo == "Suite"


def test_room_que_no_existe_lanza_error():
    with pytest.raises(RoomNoEncontradaError):
        hacer_rooms([]).buscar(99)


# pruebas de usuarios

def test_encuentra_usuario_por_id():
    usuarios = [Usuario(id_user=1, name="Maria", edad=30, sexo="F", telefono="123", email="m@m.com")]
    assert hacer_usuarios(usuarios).buscar(1).name == "Maria"


def test_usuario_que_no_existe_lanza_error():
    with pytest.raises(UsuarioNoEncontradoError):
        hacer_usuarios([]).buscar(5)


def test_email_sin_arroba_lanza_error():
    u = Usuario(id_user=1, name="Juan", edad=25, sexo="M", telefono="123", email="noesvalido")
    with pytest.raises(DatosInvalidosError):
        hacer_usuarios([]).registrar(u)


def test_telefono_vacio_lanza_error():
    u = Usuario(id_user=1, name="Juan", edad=25, sexo="M", telefono="   ", email="j@j.com")
    with pytest.raises(DatosInvalidosError):
        hacer_usuarios([]).registrar(u)


# pruebas de reservas

def test_reserva_calcula_bien_el_total():
    room = Room(id=1, tipo="Sencilla", precio=50.0, reservada_por=None)
    usuario = Usuario(id_user=1, name="Maria", edad=30, sexo="F", telefono="123", email="m@m.com")
    reserva = hacer_reservas([], [room], [usuario]).crear(1, 1, 3)
    assert reserva.total == 150.0


def test_no_se_puede_reservar_room_ocupada():
    room = Room(id=1, tipo="Sencilla", precio=50.0, reservada_por=2)
    usuario = Usuario(id_user=1, name="Maria", edad=30, sexo="F", telefono="123", email="m@m.com")
    with pytest.raises(RoomNoDisponibleError):
        hacer_reservas([], [room], [usuario]).crear(1, 1, 2)


def test_horas_en_cero_lanza_error():
    room = Room(id=1, tipo="Sencilla", precio=50.0, reservada_por=None)
    usuario = Usuario(id_user=1, name="Maria", edad=30, sexo="F", telefono="123", email="m@m.com")
    with pytest.raises(DatosInvalidosError):
        hacer_reservas([], [room], [usuario]).crear(1, 1, 0)


def test_cancelar_reserva_que_no_existe():
    with pytest.raises(ReservaNoEncontradaError):
        hacer_reservas([], [], []).cancelar(999)