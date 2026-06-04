"""
Pydantic schemas for User validation and serialization.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator


class UsuarioBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    edad: int = Field(..., description="El usuario debe ser mayor de edad")
    sexo: str = Field(..., description="Debe ser M, F u Otro")
    telefono: str = Field(..., min_length=1)
    email: EmailStr

    @field_validator("edad")
    @classmethod
    def _validar_edad(cls, v: int) -> int:
        if v < 18:
            raise ValueError("El usuario debe ser mayor de edad")
        return v

    @field_validator("sexo")
    @classmethod
    def _validar_sexo(cls, v: str) -> str:
        if isinstance(v, str):
            if v.lower() in ("masculino", "hombre"):
                v = "M"
            elif v.lower() in ("femenino", "mujer"):
                v = "F"
        
        if v not in ("M", "F", "Otro"):
            raise ValueError("Sexo inválido. Debe ser M, F u Otro")
        return v

    @field_validator("telefono")
    @classmethod
    def _validar_telefono(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El teléfono no puede estar vacío o contener solo espacios")
        return v.strip()


class UsuarioCreate(UsuarioBase):
    """Schema for creating a new user (without ID)."""
    pass


class UsuarioResponse(UsuarioBase):
    """Schema for returning user data (including database auto-generated ID)."""
    id_user: int

    model_config = {"from_attributes": True}