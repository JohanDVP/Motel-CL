from dataclasses import dataclass, field

@dataclass
class Usuario: #cliente del motel
    id_user: int
    name: str
    edad: int
    sexo: str
    telefono: str
    email: str

@dataclass
class Room: #Habitacion
    id: int
    tipo: str
    precio: float
    caracteristicas: list[str] = field(default_factory=list)
    reservada_por: int|None = None #puedo no estar reservada

@dataclass
class Reserva: #reserva de cliente
    id: int
    id_usuario: int
    id_room: int
    horas: int
    total: float
    estado: str = "activa"
    


