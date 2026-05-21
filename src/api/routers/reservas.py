from fastapi import APIRouter, HTTPException
from app.services import ReservaService, UsuarioService, RoomService
from app.storage import ReservaStorage, UsuarioStorage, RoomStorage
from app.exceptions import *

router = APIRouter(prefix="/reservas", tags=["Reservas"])

_usuario = UsuarioService(UsuarioStorage())
_alojamiento = RoomService(RoomStorage())
_res = ReservaService(ReservaStorage(), _alojamiento, _usuario)
@router.get("/")
def listar():
    return _res.listar()


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


@router.delete("/{reserva_id}")
def cancelar(reserva_id: int):
    try:
        _res.cancelar(reserva_id)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

from api.schemas.reserva import ReservaResponse

@router.get("/", response_model=list[ReservaResponse])
def listar():
    return _res.listar()

@router.put("/{reserva_id}")
def actualizar(reserva_id: int, data: dict):
    reservas = _res.listar()

    for r in reservas:
        if r.identificacion == reserva_id:
            r.horas = data.get("horas", r.horas)
            return r

    raise HTTPException(status_code=404, detail="Reserva no encontrada")

@router.get("/{reserva_id}")
def obtener(reserva_id: int):
    reservas = _res.listar()

    for r in reservas:
        if r.identificacion == reserva_id:
            return r

    raise HTTPException(status_code=404, detail="Reserva no encontrada")
