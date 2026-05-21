from pydantic import BaseModel

class RoomResponse(BaseModel):
    identificacion: int
    tipo: str
    precio: float
    caracteristicas: list[str]
    reservada_por: int | None
    disponible: bool

    class Config:
        from_attributes = True