"""
User Repository implementation using Supabase.
"""

from supabase import Client
from src.schemas.user import UsuarioCreate, UsuarioResponse


class UserRepository:
    def __init__(self, client: Client):
        self.client = client
        self.table = "usuarios"

    def create(self, user_data: UsuarioCreate) -> UsuarioResponse:
        """Inserta un nuevo usuario en la base de datos."""
        payload = user_data.model_dump()
        response = self.client.table(self.table).insert(payload).execute()
        return UsuarioResponse.model_validate(response.data[0])

    def get_all(self) -> list[UsuarioResponse]:
        """Obtiene todos los usuarios registrados."""
        response = self.client.table(self.table).select("*").execute()
        return [UsuarioResponse.model_validate(user) for user in response.data]

    def get_by_id(self, id_user: int) -> UsuarioResponse | None:
        """Busca un usuario por su ID único."""
        response = self.client.table(self.table).select("*").eq("id_user", id_user).execute()
        if not response.data:
            return None
        return UsuarioResponse.model_validate(response.data[0])