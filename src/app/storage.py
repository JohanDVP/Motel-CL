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


def _upsert(lista: list[dict], nuevo: dict, clave: str) -> list[dict]:
    """Inserta o actualiza un elemento en la lista por clave."""
    for i, item in enumerate(lista):
        if item[clave] == nuevo[clave]:
            lista[i] = nuevo
            return lista
    lista.append(nuevo)
    return lista


class UsuarioStorage:

    def obtener_todos(self) -> list[Usuario]:
        return [
            Usuario(
                id_user=u["id"],
                name=u["name"],
                edad=u["edad"],
                sexo=u["sexo"],
                telefono=u["telefono"],
                email=u["email"],
            )
            for u in _leer().get("usuarios", [])
        ]

    def guardar(self, u: Usuario) -> None:
        data = _leer()
        nuevo = {
            "id": u.id_user,
            "name": u.name,
            "edad": u.edad,
            "sexo": u.sexo,
            "telefono": u.telefono,
            "email": u.email,
        }
        data["usuarios"] = _upsert(data.get("usuarios", []), nuevo, "id")
        _guardar(data)


class RoomStorage:

    def obtener_todas(self) -> list[Room]:
        return [
            Room(
                id=r["id"],
                tipo=r["tipo"],
                precio=r["precio"],
                caracteristicas=r["caracteristicas"],
                reservada_por=r.get("reservada_por"),
            )
            for r in _leer().get("rooms", [])
        ]

    def guardar(self, r: Room) -> None:
        data = _leer()
        nuevo = {
            "id": r.id,
            "tipo": r.tipo,
            "precio": r.precio,
            "caracteristicas": r.caracteristicas,
            "reservada_por": r.reservada_por,
        }
        data["rooms"] = _upsert(data.get("rooms", []), nuevo, "id")
        _guardar(data)


class ReservaStorage:

    def obtener_todas(self) -> list[Reserva]:
        return [
            Reserva(
                id=r["id"],
                id_usuario=r["id_usuario"],
                id_room=r["id_room"],
                horas=r["horas"],
                total=r["total"],
                estado=r.get("estado", "activa"),
            )
            for r in _leer().get("reservas", [])
        ]

    def guardar(self, r: Reserva) -> None:
        data = _leer()
        nuevo = {
            "id": r.id,
            "id_usuario": r.id_usuario,
            "id_room": r.id_room,
            "horas": r.horas,
            "total": r.total,
            "estado": r.estado,
        }
        data["reservas"] = _upsert(data.get("reservas", []), nuevo, "id")
        _guardar(data)