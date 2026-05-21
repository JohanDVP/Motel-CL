from fastapi import APIRouter, HTTPException
from app.services import UsuarioService
from app.storage import UsuarioStorage
from app.models import Usuario
from app.exceptions import DatosInvalidosError
from api.schemas.user import UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

service = UsuarioService(UsuarioStorage())
@router.get("/")
def listar():
    return service.listar()


@router.post("/")
def crear(data: dict):
    try:
        nuevo_id = max([u.id_usuario for u in service.listar()], default=0) + 1

        usuario = Usuario(
            id_usuario=nuevo_id,
            nombre=data["nombre"],
            edad=data["edad"],
            sexo=data["sexo"],
            telefono=data["telefono"],
            correo=data["correo"]
        )

        service.registrar(usuario)
        return usuario

    except DatosInvalidosError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}")
def actualizar(user_id: int, data: UserUpdate):
    usuarios = service.listar()

    for u in usuarios:
        if u.id_usuario == user_id:

            update_data = data.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(u, key, value)

            return u

    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.get("/{user_id}")
def obtener(user_id: int):
    usuarios = service.listar()

    for u in usuarios:
        if u.id_usuario == user_id:
            return u

    raise HTTPException(status_code=404, detail="Usuario no encontrado")
