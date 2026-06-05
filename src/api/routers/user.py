"""Router de FastAPI para los endpoints de Usuarios."""

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_user_service
from src.core.exceptions import MotelError, UsuarioNoEncontradoError
from src.schemas.user import UsuarioCreate, UsuarioResponse
from src.services.user_service import UsuarioService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(service: UsuarioService = Depends(get_user_service)):
    """Obtiene la lista completa de usuarios registrados.

    Returns:
        list[UsuarioResponse]: Una lista con los perfiles de usuario.
    """
    return service.listar()


@router.get("/{id_user}", response_model=UsuarioResponse)
def buscar_usuario(id_user: int, service: UsuarioService = Depends(get_user_service)):
    """Busca un usuario específico por su ID.

    Args:
        id_user (int): El ID único del usuario.

    Raises:
        HTTPException: Si el usuario no es encontrado (404).

    Returns:
        UsuarioResponse: El usuario solicitado.
    """
    try:
        return service.buscar(id_user)
    except UsuarioNoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(
    usuario: UsuarioCreate, service: UsuarioService = Depends(get_user_service)
):
    """Registra un nuevo usuario en el sistema.

    Args:
        usuario (UsuarioCreate): Datos del nuevo usuario a registrar.

    Raises:
        HTTPException: Si los datos son inválidos (400).

    Returns:
        UsuarioResponse: El usuario recién registrado.
    """
    try:
        return service.registrar(usuario)
    except MotelError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.put("/{id_user}", response_model=UsuarioResponse)
def actualizar_usuario(
    id_user: int,
    usuario: UsuarioCreate,
    service: UsuarioService = Depends(get_user_service),
):
    """Actualiza los detalles del perfil de un usuario existente.

    Args:
        id_user (int): El ID del usuario a actualizar.
        usuario (UsuarioCreate): Nuevos datos del perfil de usuario.

    Raises:
        HTTPException: Si el usuario no existe (404) o los datos son inválidos (400).

    Returns:
        UsuarioResponse: El objeto de usuario actualizado.
    """
    try:
        return service.actualizar(id_user, usuario)
    except UsuarioNoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except MotelError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.delete("/{id_user}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_user: int, service: UsuarioService = Depends(get_user_service)):
    """Elimina un usuario de la base de datos.

    Args:
        id_user (int): El ID del usuario a eliminar.

    Raises:
        HTTPException: Si el usuario no existe (404) o no se puede eliminar (400).
    """
    try:
        service.eliminar(id_user)
    except UsuarioNoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except MotelError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e