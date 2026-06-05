"""Implementación del Repositorio de Reservas utilizando Supabase."""

from supabase import Client

from src.schemas.reserva import ReservaResponse


class ReservationRepository:
    """Clase de repositorio para gestionar registros de reservas en Supabase."""

    def __init__(self, client: Client) -> None:
        """Inicializa el repositorio con una instancia del cliente de Supabase.

        Args:
            client (Client): El cliente autenticado de Supabase.
        """
        self.client = client
        self.table = "reservas"

    def create(self, reservation_data: dict) -> ReservaResponse:
        """Inserta un nuevo registro de reserva en la base de datos.

        Args:
            reservation_data (dict): Diccionario que contiene los detalles
                de la reserva.

        Returns:
            ReservaResponse: El objeto de reserva validado que se ha creado.
        """
        response = self.client.table(self.table).insert(reservation_data).execute()
        return ReservaResponse.model_validate(response.data[0])

    def get_all(self) -> list[ReservaResponse]:
        """Recupera el historial completo de reservas desde la base de datos.

        Returns:
            list[ReservaResponse]: Una lista de todos los objetos de reserva
                existentes.
        """
        response = self.client.table(self.table).select("*").execute()
        return [ReservaResponse.model_validate(res) for res in response.data]

    def get_by_id(self, id_reserva: int) -> ReservaResponse | None:
        """Busca una reserva específica por su identificador único.

        Args:
            id_reserva (int): El ID de la reserva a recuperar.

        Returns:
            ReservaResponse | None: El objeto de reserva si se encuentra,
                de lo contrario None.
        """
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("id", id_reserva)
            .execute()
        )
        if not response.data:
            return None
        return ReservaResponse.model_validate(response.data[0])

    def update_status(self, id_reserva: int, nuevo_estado: str) -> ReservaResponse:
        """Actualiza el campo de estado de una reserva existente.

        Args:
            id_reserva (int): El ID de la reserva a actualizar.
            nuevo_estado (str): El nuevo estado (ej. 'activa', 'cancelada').

        Returns:
            ReservaResponse: El objeto de reserva actualizado.
        """
        response = (
            self.client.table(self.table)
            .update({"estado": nuevo_estado})
            .eq("id", id_reserva)
            .execute()
        )
        return ReservaResponse.model_validate(response.data[0])

    def update(self, id_reserva: int, reservation_data: dict) -> ReservaResponse:
        """Actualiza los campos de datos estructurales de una reserva existente.

        Args:
            id_reserva (int): El ID de la reserva a actualizar.
            reservation_data (dict): Diccionario con los campos a actualizar.

        Returns:
            ReservaResponse: El objeto de reserva actualizado.
        """
        response = (
            self.client.table(self.table)
            .update(reservation_data)
            .eq("id", id_reserva)
            .execute()
        )
        return ReservaResponse.model_validate(response.data[0])

    def delete(self, id_reserva: int) -> None:
        """Elimina permanentemente un registro de reserva de la base de datos.

        Args:
            id_reserva (int): El ID de la reserva a eliminar.
        """
        self.client.table(self.table).delete().eq("id", id_reserva).execute()