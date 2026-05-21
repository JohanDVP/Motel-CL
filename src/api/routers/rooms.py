from fastapi import APIRouter
from app.services import RoomService
from app.storage import RoomStorage
from fastapi import HTTPException

router = APIRouter(prefix="/rooms", tags=["Rooms"])

service = RoomService(RoomStorage())
@router.get("/")
def listar():
    return service.listar()


@router.get("/disponibles")
def disponibles():
    return service.listar_disponibles()

from api.schemas.room import RoomResponse
from typing import List

@router.get("/", response_model=List[RoomResponse])
def listar():
    return service.listar()

@router.put("/{room_id}")
def actualizar(room_id: int, data: dict):
    rooms = service.listar()

    for r in rooms:
        if r.identificacion == room_id:
            r.precio = data.get("precio", r.precio)
            return r

    raise HTTPException(status_code=404, detail="Room no encontrada")

@router.get("/{room_id}")
def obtener(room_id: int):
    rooms = service.listar()

    for r in rooms:
        if r.identificacion == room_id:
            return r

    raise HTTPException(status_code=404, detail="Room no encontrada")