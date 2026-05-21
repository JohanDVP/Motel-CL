from pydantic import BaseModel

class ReservaResponse(BaseModel):
    identificacion: int
    id_usuario: int
    id_room: int
    horas: int
    total: float
    estado: str

    class Config:
        from_attributes = True