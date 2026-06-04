"""
FastAPI router for User endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from src.services.user_service import UsuarioService
from src.schemas.user import UsuarioCreate, UsuarioResponse
from src.core.exceptions import UsuarioNoEncontradoError, MotelError
from src.api.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(service: UsuarioService = Depends(get_user_service)):
    """Retrieves the complete list of users."""
    return service.listar()


@router.get("/{id_user}", response_model=UsuarioResponse)
def buscar_usuario(id_user: int, service: UsuarioService = Depends(get_user_service)):
    """Retrieves a single user by their ID."""
    try:
        return service.buscar(id_user)
    except UsuarioNoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(
    usuario: UsuarioCreate, 
    service: UsuarioService = Depends(get_user_service)
):
    """Registers a new user into the system."""
    try:
        return service.registrar(usuario)
    except MotelError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_user}", response_model=UsuarioResponse)
def actualizar_usuario(
    id_user: int,
    usuario: UsuarioCreate,
    service: UsuarioService = Depends(get_user_service)
):
    """Updates an existing user's profiles details."""
    try:
        return service.actualizar(id_user, usuario)
    except UsuarioNoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MotelError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id_user}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_user: int, service: UsuarioService = Depends(get_user_service)):
    """Deletes a user from the database."""
    try:
        service.eliminar(id_user)
    except UsuarioNoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MotelError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))