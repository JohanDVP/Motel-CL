"""
FastAPI router for User endpoints.
"""

from fastapi import APIRouter, HTTPException, status
from src.storage.base import get_supabase_client
from src.storage.user_repository import UserRepository
from src.services.user_service import UsuarioService
from src.schemas.user import UsuarioCreate, UsuarioResponse
from src.core.exceptions import UsuarioNoEncontradoError

router = APIRouter(prefix="/users", tags=["Users"])


def _get_service() -> UsuarioService:
    """Helper to inject dependencies manually without complex setup."""
    client = get_supabase_client()
    repo = UserRepository(client)
    return UsuarioService(repo)


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios():
    service = _get_service()
    return service.listar()


@router.get("/{id_user}", response_model=UsuarioResponse)
def buscar_usuario(id_user: int):
    service = _get_service()
    try:
        return service.buscar(id_user)
    except UsuarioNoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate):
    service = _get_service()
    try:
        return service.registrar(usuario)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))