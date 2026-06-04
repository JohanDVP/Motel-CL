"""
Business logic service for managing motel rooms.
"""

from src.storage.room_repository import RoomRepository
from src.schemas.room import RoomResponse
from src.core.exceptions import RoomNoEncontradaError


class RoomService:
    def __init__(self, repository: RoomRepository) -> None:
        self._repository = repository

    def listar(self) -> list[RoomResponse]:
        """Retrieves all rooms in the motel."""
        return self._repository.get_all()

    def listar_disponibles(self) -> list[RoomResponse]:
        """Filters and retrieves only unreserved rooms."""
        return [r for r in self._repository.get_all() if r.reservada_por is None]

    def buscar(self, id_room: int) -> RoomResponse:
        """
        Finds a room by its ID.
        
        Raises:
            RoomNoEncontradaError: If the room doesn't exist.
        """
        room = self._repository.get_by_id(id_room)
        if room is None:
            raise RoomNoEncontradaError(f"La habitación con ID {id_room} no existe.")
        return room