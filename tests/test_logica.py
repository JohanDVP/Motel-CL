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


# ── Helpers ──────────────────────────────────────────────────────────────────

def hacer_rooms(rooms: list[Room]) -> RoomService:
    storage = MagicMock()
    storage.obtener_todas.return_value = rooms
    return RoomService(storage)


def hacer_usuarios(usuarios: list[Usuario]) -> UsuarioService:
    storage = MagicMock()
    storage.obtener_todos.return_value = usuarios
    return UsuarioService(storage)


def hacer_reservas(
    reservas: list[Reserva],
    rooms: list[Room],
    usuarios: list[Usuario],
) -> ReservaService:
    storage = MagicMock()
    storage.obtener_todas.return_value = reservas
    return ReservaService(storage, hacer_rooms(rooms), hacer_usuarios(usuarios))


def usuario_valido(**kwargs) -> Usuario:
    defaults = dict(id_user=1, name="Maria", edad=30, sexo="F", telefono="123", email="m@m.com")
    return Usuario(**{**defaults, **kwargs})


def room_disponible(**kwargs) -> Room:
    defaults = dict(id=1, tipo="Sencilla", precio=50.0, reservada_por=None)
    return Room(**{**defaults, **kwargs})


# ── Habitaciones ─────────────────────────────────────────────────────────────

def test_solo_muestra_rooms_disponibles():
    rooms = [
        room_disponible(id=1, reservada_por=None),
        room_disponible(id=2, reservada_por=1),
    ]
    assert len(hacer_rooms(rooms).listar_disponibles()) == 1


def test_encuentra_room_por_id():
    rooms = [room_disponible(id=3, tipo="Suite")]
    assert hacer_rooms(rooms).buscar(3).tipo == "Suite"


def test_room_que_no_existe_lanza_error():
    with pytest.raises(RoomNoEncontradaError):
        hacer_rooms([]).buscar(99)


# ── Usuarios ─────────────────────────────────────────────────────────────────

def test_encuentra_usuario_por_id():
    usuarios = [usuario_valido()]
    assert hacer_usuarios(usuarios).buscar(1).name == "Maria"


def test_usuario_que_no_existe_lanza_error():
    with pytest.raises(UsuarioNoEncontradoError):
        hacer_usuarios([]).buscar(5)


def test_email_sin_arroba_lanza_error():
    svc = hacer_usuarios([])
    with pytest.raises(DatosInvalidosError):
        svc._validar_email("noesvalido")


def test_service_email_invalido():
    svc = hacer_usuarios([])
    with pytest.raises(DatosInvalidosError):
        svc._validar_email("noesvalido")


def test_service_telefono_vacio():
    svc = hacer_usuarios([])
    with pytest.raises(DatosInvalidosError):
        svc._validar_telefono("   ")


# ── Reservas ─────────────────────────────────────────────────────────────────

def test_reserva_calcula_bien_el_total():
    room = room_disponible(precio=50.0)
    usuario = usuario_valido()
    reserva = hacer_reservas([], [room], [usuario]).crear(1, 1, 3)
    assert reserva.total == 150.0


def test_no_se_puede_reservar_room_ocupada():
    room = room_disponible(reservada_por=2)
    usuario = usuario_valido()
    with pytest.raises(RoomNoDisponibleError):
        hacer_reservas([], [room], [usuario]).crear(1, 1, 2)


def test_horas_en_cero_lanza_error():
    room = room_disponible()
    usuario = usuario_valido()
    with pytest.raises(DatosInvalidosError):
        hacer_reservas([], [room], [usuario]).crear(1, 1, 0)


def test_cancelar_reserva_que_no_existe():
    with pytest.raises(ReservaNoEncontradaError):
        hacer_reservas([], [], []).cancelar(999)


def test_cancelar_reserva_inactiva_lanza_error():
    reserva = Reserva(id=1, id_usuario=1, id_room=1, horas=2, total=100.0, estado="cancelada")
    room = room_disponible()
    usuario = usuario_valido()
    with pytest.raises(DatosInvalidosError):
        hacer_reservas([reserva], [room], [usuario]).cancelar(1)