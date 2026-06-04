"""
Pydantic schemas for Reservation validation and serialization.
"""

from typing import Literal
from pydantic import BaseModel, Field

ESTADOS_VALIDOS = Literal["activa", "cancelada", "completada"]


class ReservaBase(BaseModel):
    id_usuario: int
    id_room: int
    horas: int = Field(..., gt=0, description="Las horas deben ser mayores a 0")
    total: float = Field(..., ge=0, description="El total no puede ser negativo")
    estado: ESTADOS_VALIDOS = "activa"


class ReservaCreate(BaseModel):
    """Schema used when a client requests a new reservation."""
    id_usuario: int
    id_room: int
    horas: int = Field(..., gt=0)


class ReservaResponse(ReservaBase):
    """Schema for returning complete reservation details."""
    id: int

    model_config = {"from_attributes": True}

    @property
    def activa(self) -> bool:
        return self.estado == "activa"