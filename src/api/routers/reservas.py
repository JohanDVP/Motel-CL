from fastapi import APIRouter, HTTPException
from src.app.services import ReservaService, UsuarioService, RoomService
from src.app.storage import ReservaStorage, UsuarioStorage, RoomStorage
from src.app.exceptions import *
from src.api.schemas.reserva import ReservaResponse

router = APIRouter(prefix="/reservas", tags=["Reservas"])

_usuario = UsuarioService(UsuarioStorage())
_alojamiento = RoomService(RoomStorage())
_res = ReservaService(ReservaStorage(), _alojamiento, _usuario)

# Lista todas las reservas mapeadas al esquema de Pydantic
@router.get("/", response_model=list[ReservaResponse])
def listar():
    return _res.listar()

# Crea una nueva reserva en el sistema
@router.post("/")
def crear(data: dict):
    try:
        return _res.crear(
            data["id_usuario"],
            data["id_room"],
            data["horas"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Cancela una reserva existente por su ID real
@router.delete("/{reserva_id}")
def cancelar(reserva_id: int):
    try:
        _res.cancelar(reserva_id)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Actualiza las horas de una reserva usando su ID correcto de dataclass
@router.put("/{reserva_id}")
def actualizar(reserva_id: int, data: dict):
    try:
        reservas = _res.listar()
        for r in reservas:
            # Se cambia r.identificacion por r.id para acoplarlo al modelo Reserva
            if r.id == reserva_id:
                r.horas = data.get("horas", r.horas)
                
                # Ejecutamos el validador interno del modelo automáticamente por seguridad
                r.__post_init__()
                
                return r
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
        
    except ValueError as e:
        # Captura si mandan horas en cero o negativas gracias al __post_init__
        raise HTTPException(status_code=400, detail=str(e))

# Obtiene una reserva específica por su ID
@router.get("/{reserva_id}")
def obtener(reserva_id: int):
    reservas = _res.listar()
    for r in reservas:
        # Se cambia r.identificacion por r.id
        if r.id == reserva_id:
            return r
    raise HTTPException(status_code=404, detail="Reserva no encontrada")