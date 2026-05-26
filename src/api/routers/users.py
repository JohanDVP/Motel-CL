from fastapi import APIRouter, HTTPException
# Se agrega "src." a las importaciones para solucionar el error de Python en WSL
from src.app.services import UsuarioService
from src.app.storage import UsuarioStorage
from src.app.models import Usuario
from src.app.exceptions import DatosInvalidosError
from src.api.schemas.user import UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

service = UsuarioService(UsuarioStorage())

@router.get("/")
def listar():
    return service.listar()

@router.post("/")
def crear(data: dict):
    try:
        # Se cambia u.id_usuario por u.id_user para que coincida con el modelo
        nuevo_id = max([u.id_user for u in service.listar()], default=0) + 1

        # Mapeamos lo que viene en el JSON ("nombre", "correo") a lo que pide el modelo (name, email)
        usuario = Usuario(
            id_user=nuevo_id,
            name=data["nombre"],
            edad=data["edad"],
            sexo=data["sexo"],
            telefono=data["telefono"],
            email=data["correo"]
        )

        service.registrar(usuario)
        return usuario
        
    except ValueError as e:
        # Captura los errores de validación de tu __post_init__ (ej: menor de edad, sexo inválido, etc.)
        raise HTTPException(status_code=400, detail=str(e))
    except DatosInvalidosError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el mapeo: {str(e)}")

@router.put("/{user_id}")
def actualizar(user_id: int, data: UserUpdate):
    usuarios = service.listar()
    for u in usuarios:
        # Se corrige a u.id_user
        if u.id_user == user_id:
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(u, key, value)
            return u
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.get("/{user_id}")
def obtener(user_id: int):
    usuarios = service.listar()
    for u in usuarios:
        # Se corrige a u.id_user
        if u.id_user == user_id:
            return u
    raise HTTPException(status_code=404, detail="Usuario no encontrado")