"""
Unit tests for the data models.

Verifies correct creation, default values, properties,
and validation errors for Usuario, Room, and Reserva.
"""

import pytest
from src.app.models import Usuario, Room, Reserva


# ── Usuario ──────────────────────────────────────────────────────────────────

def test_usuario_se_crea_bien():
    u = Usuario(id_user=1, name="Maria", edad=30, sexo="F", telefono="123", email="m@m.com")
    assert u.name == "Maria"
    assert u.id_user == 1


def test_usuario_email_invalido_lanza_error():
    with pytest.raises(ValueError, match="Email invalido"):
        Usuario(id_user=1, name="Juan", edad=25, sexo="M", telefono="123", email="noesvalido")


def test_usuario_telefono_vacio_lanza_error():
    with pytest.raises(ValueError, match="telefono"):
        Usuario(id_user=1, name="Juan", edad=25, sexo="M", telefono="   ", email="j@j.com")


def test_usuario_menor_de_edad_lanza_error():
    with pytest.raises(ValueError, match="mayor de edad"):
        Usuario(id_user=1, name="Niño", edad=15, sexo="M", telefono="123", email="a@a.com")


def test_usuario_sexo_invalido_lanza_error():
    with pytest.raises(ValueError, match="Sexo invalido"):
        Usuario(id_user=1, name="Juan", edad=25, sexo="X", telefono="123", email="j@j.com")


# ── Room ─────────────────────────────────────────────────────────────────────

def test_room_sin_reserva_por_defecto():
    r = Room(id=1, tipo="Sencilla", precio=50.0)
    assert r.reservada_por is None


def test_room_disponible_property():
    r = Room(id=1, tipo="Sencilla", precio=50.0)
    assert r.disponible is True


def test_room_ocupada_property():
    r = Room(id=1, tipo="Sencilla", precio=50.0, reservada_por=1)
    assert r.disponible is False


def test_room_caracteristicas_vacias_por_defecto():
    r = Room(id=1, tipo="Sencilla", precio=50.0)
    assert r.caracteristicas == []


def test_room_tipo_invalido_lanza_error():
    with pytest.raises(ValueError, match="Tipo de habitacion invalido"):
        Room(id=1, tipo="Penthouse", precio=50.0)


def test_room_precio_cero_lanza_error():
    with pytest.raises(ValueError, match="precio"):
        Room(id=1, tipo="Suite", precio=0)


# ── Reserva ──────────────────────────────────────────────────────────────────

def test_reserva_estado_activa_por_defecto():
    r = Reserva(id=1, id_usuario=1, id_room=1, horas=2, total=100.0)
    assert r.estado == "activa"


def test_reserva_activa_property():
    r = Reserva(id=1, id_usuario=1, id_room=1, horas=2, total=100.0)
    assert r.activa is True


def test_reserva_cancelada_property():
    r = Reserva(id=1, id_usuario=1, id_room=1, horas=2, total=100.0, estado="cancelada")
    assert r.activa is False


def test_reserva_guarda_total_correcto():
    r = Reserva(id=1, id_usuario=1, id_room=1, horas=2, total=100.0)
    assert r.total == 100.0


def test_reserva_horas_cero_lanza_error():
    with pytest.raises(ValueError, match="horas"):
        Reserva(id=1, id_usuario=1, id_room=1, horas=0, total=0.0)


def test_reserva_estado_invalido_lanza_error():
    with pytest.raises(ValueError, match="Estado invalido"):
        Reserva(id=1, id_usuario=1, id_room=1, horas=2, total=100.0, estado="pendiente")