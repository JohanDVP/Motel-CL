"""
Pydantic schemas for Room validation and serialization.
"""

from typing import Literal
from pydantic import BaseModel, Field

TIPOS_VALIDOS = Literal["Sencilla", "Doble", "Suite", "Jacuzzi"]


class RoomBase(BaseModel):
    tipo: TIPOS_VALIDOS
    precio: float = Field(..., gt=0, description="El precio debe ser mayor a 0")
    caracteristicas: list[str] = Field(default_factory=list)
    reservada_por: int | None = None


class RoomCreate(RoomBase):
    """Schema for creating a new room."""
    pass


class RoomResponse(RoomBase):
    """Schema for returning room data."""
    id: int

    model_config = {"from_attributes": True}

    @property
    def disponible(self) -> bool:
        return self.reservada_por is None