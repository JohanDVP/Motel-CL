"""
Business logic service handling motel room management and status updates.
"""

from src.storage.room_repository import RoomRepository
from src.schemas.room import RoomCreate, RoomResponse
from src.core.exceptions import RoomNoEncontradaError


class RoomService:
    def __init__(self, repository: RoomRepository) -> None:
        self._repository = repository

    def listar(self) -> list[RoomResponse]:
        """Retrieves all rooms from the database."""
        return self._repository.get_all()

    def listar_disponibles(self) -> list[RoomResponse]:
        """Retrieves only available rooms (where reservada_por is NULL)."""
        return self._repository.get_available()

    def buscar(self, room_id: int) -> RoomResponse:
        """
        Finds a room by its ID. 
        Raises RoomNoEncontradaError if the room does not exist.
        """
        room = self._repository.get_by_id(room_id)
        if room is None:
            raise RoomNoEncontradaError(f"La habitación con ID {room_id} no existe.")
        return room

    def crear(self, room_data: RoomCreate) -> RoomResponse:
        """Creates a new room entry into the system."""
        return self._repository.create(room_data)

    def actualizar(self, room_id: int, room_data: RoomCreate) -> RoomResponse:
        """Updates an existing room's features or price."""
        self.buscar(room_id)  # Valida existencia
        return self._repository.update(room_id, room_data)

    def eliminar(self, room_id: int) -> None:
        """Deletes a room from the system layout."""
        self.buscar(room_id)  # Valida existencia
        self._repository.delete(room_id)

    def marcar_como_ocupada(self, room_id: int, user_id: int) -> None:
        """Public method to safely change a room's status to occupied by a user."""
        self.buscar(room_id)
        self._repository.update_reservation(room_id, user_id)

    def liberar_habitacion(self, room_id: int) -> None:
        """Public method to clear room occupancy, setting the reservation holder to None."""
        self.buscar(room_id)
        self._repository.update_reservation(room_id, None)