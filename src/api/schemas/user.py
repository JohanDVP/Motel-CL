from pydantic import BaseModel

class UserResponse(BaseModel):
    id_usuario: int
    nombre: str
    edad: int
    sexo: str
    telefono: str
    correo: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    nombre: str | None = None
    edad: int | None = None
    sexo: str | None = None
    telefono: str | None = None
    correo: str | None = None
