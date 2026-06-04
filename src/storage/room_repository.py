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