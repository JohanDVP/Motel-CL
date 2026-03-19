"""
Persistence layer for the Motel system.

Handles reading and writing of users, rooms, and reservations to a JSON file.
"""

import json
from pathlib import Path

from .models import Usuario, Room, Reserva

RUTA = Path(__file__).parent.parent.parent / "data" / "datos.json"


def _leer() -> dict:
    """
    Reads the JSON data file.

    Returns:
        dict: The full data dictionary with keys 'usuarios', 'rooms', 'reservas'.
    """
    if not RUTA.exists():
        return {"usuarios": [], "rooms": [], "reservas": []}
    with RUTA.open("r", encoding="utf-8") as f:
        return json.load(f)


def _guardar(data: dict) -> None:
    """
    Writes the data dictionary to the JSON file.

    Args:
        data (dict): The full data dictionary to persist.
    """
    with RUTA.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _upsert(lista: list[dict], nuevo: dict, clave: str) -> list[dict]:
    """
    Inserts or updates an element in a list by key.

    Args:
        lista (list[dict]): The list to update.
        nuevo (dict): The new element to insert or replace.
        clave (str): The key used to match existing elements.

    Returns:
        list[dict]: The updated list.
    """
    for i, item in enumerate(lista):
        if item[clave] == nuevo[clave]:
            lista[i] = nuevo
            return lista
    lista.append(nuevo)
    return lista


class UsuarioStorage:
    """
    Handles persistence operations for Usuario entities.
    """

    def obtener_todos(self) -> list[Usuario]:
        """
        Retrieves all users from the JSON file.

        Returns:
            list[Usuario]: List of all stored users.
        """
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
        """
        Saves or updates a user in the JSON file.

        Args:
            u (Usuario): The user instance to persist.
        """
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
    """
    Handles persistence operations for Room entities.
    """

    def obtener_todas(self) -> list[Room]:
        """
        Retrieves all rooms from the JSON file.

        Returns:
            list[Room]: List of all stored rooms.
        """
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
        """
        Saves or updates a room in the JSON file.

        Args:
            r (Room): The room instance to persist.
        """
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
    """
    Handles persistence operations for Reserva entities.
    """

    def obtener_todas(self) -> list[Reserva]:
        """
        Retrieves all reservations from the JSON file.

        Returns:
            list[Reserva]: List of all stored reservations.
        """
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
        """
        Saves or updates a reservation in the JSON file.

        Args:
            r (Reserva): The reservation instance to persist.
        """
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