"""Implementación del Repositorio de Usuarios utilizando Supabase."""

from supabase import Client

from src.schemas.user import UsuarioCreate, UsuarioResponse


class UserRepository:
    """Clase de repositorio para gestionar los usuarios en Supabase."""

    def __init__(self, client: Client) -> None:
        """Inicializa el repositorio con una instancia del cliente de Supabase.

        Args:
            client (Client): El cliente autenticado de Supabase.
        """
        self.client = client
        self.table = "usuarios"

    def create(self, user_data: UsuarioCreate) -> UsuarioResponse:
        """Inserta un nuevo usuario en la base de datos.

        Args:
            user_data (UsuarioCreate): Objeto con los datos del usuario.

        Returns:
            UsuarioResponse: El usuario recién creado y validado.
        """
        payload = user_data.model_dump()
        response = self.client.table(self.table).insert(payload).execute()
        return UsuarioResponse.model_validate(response.data[0])

    def get_all(self) -> list[UsuarioResponse]:
        """Obtiene todos los usuarios registrados.

        Returns:
            list[UsuarioResponse]: Lista con todos los objetos de usuario.
        """
        response = self.client.table(self.table).select("*").execute()
        return [UsuarioResponse.model_validate(user) for user in response.data]

    def get_by_id(self, id_user: int) -> UsuarioResponse | None:
        """Busca un usuario por su ID único.

        Args:
            id_user (int): El ID único del usuario.

        Returns:
            UsuarioResponse | None: El usuario encontrado o None si no existe.
        """
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("id_user", id_user)
            .execute()
        )
        if not response.data:
            return None
        return UsuarioResponse.model_validate(response.data[0])

    def update(self, id_user: int, user_data: UsuarioCreate) -> UsuarioResponse:
        """Actualiza los datos de un usuario existente en Supabase.

        Args:
            id_user (int): ID del usuario a actualizar.
            user_data (UsuarioCreate): Nuevos datos del usuario.

        Returns:
            UsuarioResponse: El objeto de usuario actualizado.
        """
        payload = user_data.model_dump()
        response = (
            self.client.table(self.table)
            .update(payload)
            .eq("id_user", id_user)
            .execute()
        )
        return UsuarioResponse.model_validate(response.data[0])

    def delete(self, id_user: int) -> None:
        """Elimina un usuario de la base de datos por su ID.

        Args:
            id_user (int): El ID del usuario a eliminar.
        """
        self.client.table(self.table).delete().eq("id_user", id_user).execute()