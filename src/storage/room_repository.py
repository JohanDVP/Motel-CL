"""
Room Repository implementation using Supabase.
"""

from supabase import Client
from src.schemas.room import RoomCreate, RoomResponse


class RoomRepository:
    def __init__(self, client: Client):
        self.client = client
        self.table = "rooms"

    def get_all(self) -> list[RoomResponse]:
        """Obtiene todas las habitaciones del motel."""
        response = self.client.table(self.table).select("*").execute()
        return [RoomResponse.model_validate(room) for room in response.data]

    def get_by_id(self, id_room: int) -> RoomResponse | None:
        """Busca una habitación específica por su ID."""
        response = self.client.table(self.table).select("*").eq("id", id_room).execute()
        if not response.data:
            return None
        return RoomResponse.model_validate(response.data[0])

    def update_reservation(self, id_room: int, id_usuario: int | None) -> RoomResponse:
        """Actualiza el estado de ocupación/reserva de una habitación."""
        response = (
            self.client.table(self.table)
            .update({"reservada_por": id_usuario})
            .eq("id", id_room)
            .execute()
        )
        return RoomResponse.model_validate(response.data[0])

    # NUEVO: Filtra habitaciones donde reservada_por sea NULL (Disponibles)
    def get_available(self) -> list[RoomResponse]:
        """Obtiene únicamente las habitaciones que no están reservadas."""
        response = (
            self.client.table(self.table)
            .select("*")
            .is_("reservada_por", "null")
            .execute()
        )
        return [RoomResponse.model_validate(room) for room in response.data]

    # NUEVO: Soporte para crear habitaciones
    def create(self, room_data: RoomCreate) -> RoomResponse:
        """Inserta una nueva habitación en la base de datos."""
        payload = room_data.model_dump()
        response = self.client.table(self.table).insert(payload).execute()
        return RoomResponse.model_validate(response.data[0])

    # NUEVO: Soporte para actualizar configuraciones o precios
    def update(self, id_room: int, room_data: RoomCreate) -> RoomResponse:
        """Actualiza los detalles técnicos o precio de una habitación existente."""
        payload = room_data.model_dump()
        response = (
            self.client.table(self.table)
            .update(payload)
            .eq("id", id_room)
            .execute()
        )
        return RoomResponse.model_validate(response.data[0])

    # NUEVO: Soporte para eliminar registros físicos
    def delete(self, id_room: int) -> None:
        """Elimina permanentemente una habitación del sistema."""
        self.client.table(self.table).delete().eq("id", id_room).execute()