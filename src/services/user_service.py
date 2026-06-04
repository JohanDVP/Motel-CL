"""
Business logic service for managing motel clients.
"""

from src.storage.user_repository import UserRepository
from src.schemas.user import UsuarioCreate, UsuarioResponse
from src.core.exceptions import UsuarioNoEncontradoError


class UsuarioService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def listar(self) -> list[UsuarioResponse]:
        """Retrieves all registered users from the database."""
        return self._repository.get_all()

    def buscar(self, id_user: int) -> UsuarioResponse:
        """
        Finds a user by their unique database ID.
        
        Raises:
            UsuarioNoEncontradoError: If the user doesn't exist.
        """
        usuario = self._repository.get_by_id(id_user)
        if usuario is None:
            raise UsuarioNoEncontradoError(f"El usuario con ID {id_user} no existe.")
        return usuario

    def registrar(self, usuario: UsuarioCreate) -> UsuarioResponse:
        """Registers a new user after schema validation."""
        return self._repository.create(usuario)