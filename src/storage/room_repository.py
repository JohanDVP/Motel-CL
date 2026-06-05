"""Implementación del Repositorio de Habitaciones utilizando Supabase."""

from supabase import Client

from src.schemas.room import RoomCreate, RoomResponse


class RoomRepository:
    """Clase de repositorio para gestionar las habitaciones en Supabase."""

    def __init__(self, client: Client) -> None:
        """Inicializa el repositorio con una instancia del cliente de Supabase.

        Args:
            client (Client): El cliente autenticado de Supabase.
        """
        self.client = client
        self.table = "rooms"

    def get_all(self) -> list[RoomResponse]:
        """Obtiene todas las habitaciones del motel.

        Returns:
            list[RoomResponse]: Lista de todos los objetos de habitación.
        """
        response = self.client.table(self.table).select("*").execute()
        return [RoomResponse.model_validate(room) for room in response.data]

    def get_by_id(self, id_room: int) -> RoomResponse | None:
        """Busca una habitación específica por su ID.

        Args:
            id_room (int): El identificador único de la habitación.

        Returns:
            RoomResponse | None: La habitación si existe, de lo contrario None.
        """
        response = self.client.table(self.table).select("*").eq("id", id_room).execute()
        if not response.data:
            return None
        return RoomResponse.model_validate(response.data[0])

    def update_reservation(self, id_room: int, id_usuario: int | None) -> RoomResponse:
        """Actualiza el estado de ocupación de una habitación.

        Args:
            id_room (int): El ID de la habitación.
            id_usuario (int | None): ID del usuario que reserva o None para liberar.

        Returns:
            RoomResponse: El objeto de la habitación actualizada.
        """
        response = (
            self.client.table(self.table)
            .update({"reservada_por": id_usuario})
            .eq("id", id_room)
            .execute()
        )
        return RoomResponse.model_validate(response.data[0])

    def get_available(self) -> list[RoomResponse]:
        """Obtiene únicamente las habitaciones que no están reservadas.

        Returns:
            list[RoomResponse]: Lista de habitaciones disponibles.
        """
        response = (
            self.client.table(self.table)
            .select("*")
            .is_("reservada_por", "null")
            .execute()
        )
        return [RoomResponse.model_validate(room) for room in response.data]

    def create(self, room_data: RoomCreate) -> RoomResponse:
        """Inserta una nueva habitación en la base de datos.

        Args:
            room_data (RoomCreate): Datos de la nueva habitación.

        Returns:
            RoomResponse: La habitación creada.
        """
        payload = room_data.model_dump()
        response = self.client.table(self.table).insert(payload).execute()
        return RoomResponse.model_validate(response.data[0])

    def update(self, id_room: int, room_data: RoomCreate) -> RoomResponse:
        """Actualiza los detalles técnicos o precio de una habitación existente.

        Args:
            id_room (int): ID de la habitación a actualizar.
            room_data (RoomCreate): Nuevos datos de la habitación.

        Returns:
            RoomResponse: El objeto de la habitación actualizado.
        """
        payload = room_data.model_dump()
        response = (
            self.client.table(self.table)
            .update(payload)
            .eq("id", id_room)
            .execute()
        )
        return RoomResponse.model_validate(response.data[0])

    def delete(self, id_room: int) -> None:
        """Elimina permanentemente una habitación del sistema.

        Args:
            id_room (int): ID de la habitación a eliminar.
        """
        self.client.table(self.table).delete().eq("id", id_room).execute()