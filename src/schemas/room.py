"""
Pydantic schemas for Room validation and serialization.
"""

from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

# Unificamos los tipos válidos para que coincidan con la interfaz de usuario
TIPOS_VALIDOS = Literal["Sencilla", "Doble", "Suite", "Jacuzzi"]


class RoomBase(BaseModel):
    # He cambiado el valor por defecto a None para que no falle 
    # si la columna 'numero' no existe en la base de datos.
    numero: str | None = Field(None, min_length=1, description="Número o identificador físico de la habitación")
    tipo: TIPOS_VALIDOS
    precio: float = Field(..., gt=0, description="El precio por hora debe ser mayor a 0")
    caracteristicas: list[str] = Field(default_factory=list)
    reservada_por: int | None = None


class RoomCreate(RoomBase):
    """Schema for creating a new room."""
    pass


class RoomResponse(RoomBase):
    """Schema for returning room data."""
    id: int

    model_config = ConfigDict(from_attributes=True)

    @property
    def disponible(self) -> bool:
        return self.reservada_por is None