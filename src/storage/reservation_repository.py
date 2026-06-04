"""
Reservation Repository implementation using Supabase.
"""

from supabase import Client
from src.schemas.reserva import ReservaCreate, ReservaResponse


class ReservationRepository:
    def __init__(self, client: Client):
        self.client = client
        self.table = "reservas"

    def create(self, reservation_data: dict) -> ReservaResponse:
        """Inserta una nueva reserva calculada en la base de datos."""
        response = self.client.table(self.table).insert(reservation_data).execute()
        return ReservaResponse.model_validate(response.data[0])

    def get_all(self) -> list[ReservaResponse]:
        """Obtiene el historial completo de reservas."""
        response = self.client.table(self.table).select("*").execute()
        return [ReservaResponse.model_validate(res) for res in response.data]

    def get_by_id(self, id_reserva: int) -> ReservaResponse | None:
        """Busca una reserva por su ID."""
        response = self.client.table(self.table).select("*").eq("id", id_reserva).execute()
        if not response.data:
            return None
        return ReservaResponse.model_validate(response.data[0])

    def update_status(self, id_reserva: int, nuevo_estado: str) -> ReservaResponse:
        """Cambia el estado de la reserva (activa, cancelada, completada)."""
        response = (
            self.client.table(self.table)
            .update({"estado": nuevo_estado})
            .eq("id", id_reserva)
            .execute()
        )
        return ReservaResponse.model_validate(response.data[0])