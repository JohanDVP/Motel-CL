from fastapi import APIRouter, HTTPException
from typing import List
from src.app.services import RoomService
from src.app.storage import RoomStorage
from src.api.schemas.room import RoomResponse

router = APIRouter(prefix="/rooms", tags=["Rooms"])

service = RoomService(RoomStorage())

# Lista todas las habitaciones usando el esquema de respuesta correcto
@router.get("/", response_model=List[RoomResponse])
def listar():
    return service.listar()

# Filtra y lista solo las habitaciones disponibles
@router.get("/disponibles")
def disponibles():
    return service.listar_disponibles()

# Actualiza el precio de una habitación usando su ID real
@router.put("/{room_id}")
def actualizar(room_id: int, data: dict):
    try:
        rooms = service.listar()
        for r in rooms:
            # Se cambia r.identificacion por r.id para acoplarlo al modelo
            if r.id == room_id:
                # Modificamos el precio mapeando el dato enviado
                r.precio = data.get("precio", r.precio)
                
                # Ejecutamos las validaciones del __post_init__ automáticamente 
                r.__post_init__()
                
                # Aquí deberías llamar al método de persistencia si tu servicio lo requiere, por ahora retorna el objeto modificado
                return r
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
        
    except ValueError as e:
        # Si te envían un precio negativo o igual a 0, saltará este error controlado
        raise HTTPException(status_code=400, detail=str(e))

# Obtiene una habitación específica por su ID
@router.get("/{room_id}")
def obtener(room_id: int):
    rooms = service.listar()
    for r in rooms:
        # Se cambia r.identificacion por r.id
        if r.id == room_id:
            return r
    raise HTTPException(status_code=404, detail="Habitación no encontrada")