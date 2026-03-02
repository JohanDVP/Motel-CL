import json
from pathlib import Path
from .models import Usuario, Room, Reserva

RUTA = Path(__file__).parent.parent.parent / "data" / "datos.json"


def _leer() -> dict:
    if not RUTA.exists():
        return {"usuarios": [], "rooms": [], "reservas": []}
    with RUTA.open("r", encoding="utf-8") as f:
        return json.load(f)


def _guardar(data: dict) -> None:
    with RUTA.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


class UsuarioStorage:

    def obtener_todos(self) -> list[Usuario]:
        return [Usuario(**{**u, "id_user": u["id"]}) for u in _leer().get("usuarios", [])]

    def guardar(self, u: Usuario) -> None:
        data = _leer()
        lista = data.get("usuarios", [])
        nuevo = {"id": u.id_user, "name": u.name, "edad": u.edad, "sexo": u.sexo, "telefono": u.telefono, "email": u.email}
        for i, x in enumerate(lista):
            if x["id"] == u.id_user:
                lista[i] = nuevo
                data["usuarios"] = lista
                _guardar(data)
                return
        lista.append(nuevo)
        data["usuarios"] = lista
        _guardar(data)


class RoomStorage:

    def obtener_todas(self) -> list[Room]:
        return [Room(id=r["id"], tipo=r["tipo"], precio=r["precio"], caracteristicas=r["caracteristicas"], reservada_por=r.get("reservada_por")) for r in _leer().get("rooms", [])]

    def guardar(self, r: Room) -> None:
        data = _leer()
        lista = data.get("rooms", [])
        nuevo = {"id": r.id, "tipo": r.tipo, "precio": r.precio, "caracteristicas": r.caracteristicas, "reservada_por": r.reservada_por}
        for i, x in enumerate(lista):
            if x["id"] == r.id:
                lista[i] = nuevo
                data["rooms"] = lista
                _guardar(data)
                return
        lista.append(nuevo)
        data["rooms"] = lista
        _guardar(data)


class ReservaStorage:

    def obtener_todas(self) -> list[Reserva]:
        return [Reserva(id=r["id"], id_usuario=r["id_usuario"], id_room=r["id_room"], horas=r["horas"], total=r["total"], estado=r.get("estado", "activa")) for r in _leer().get("reservas", [])]

    def guardar(self, r: Reserva) -> None:
        data = _leer()
        lista = data.get("reservas", [])
        nuevo = {"id": r.id, "id_usuario": r.id_usuario, "id_room": r.id_room, "horas": r.horas, "total": r.total, "estado": r.estado}
        for i, x in enumerate(lista):
            if x["id"] == r.id:
                lista[i] = nuevo
                data["reservas"] = lista
                _guardar(data)
                return
        lista.append(nuevo)
        data["reservas"] = lista
        _guardar(data)