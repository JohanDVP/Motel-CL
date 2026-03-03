from src.app.models import Usuario, Room, Reserva


def test_usuario_se_crea_bien():
    u = Usuario(id_user=1, name="Maria", edad=30, sexo="F", telefono="123", email="m@m.com")
    assert u.name == "Maria"
    assert u.id_user == 1


def test_room_sin_reserva_por_defecto():
    r = Room(id=1, tipo="Sencilla", precio=50.0)
    assert r.reservada_por is None


def test_room_caracteristicas_vacias_por_defecto():
    r = Room(id=1, tipo="Sencilla", precio=50.0)
    assert r.caracteristicas == []


def test_reserva_estado_activa_por_defecto():
    r = Reserva(id=1, id_usuario=1, id_room=1, horas=2, total=100.0)
    assert r.estado == "activa"


def test_reserva_guarda_total_correcto():
    r = Reserva(id=1, id_usuario=1, id_room=1, horas=2, total=100.0)
    assert r.total == 100.0