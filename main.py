import json
from typing import List
from typing import Tuple

class Usuario:
    def __init__(self,id_user: int, name: str, edad: int, sexo: str, telefono: str, email: str):
        self.id_user: int = id_user
        self.name: str = name
        self.edad: int = edad
        self.sexo: str = sexo
        self.telefono: str = telefono
        self.email: str = email
        
class Room:
    def __init__(self, id: int, tipo: str, precio: float, caracteristicas: List[str], reservada_por: str = None):
        self.id: int = id
        self.tipo: str = tipo
        self.precio: float = precio
        self.caracteristicas: List[str] = caracteristicas
        self.reservada_por: str = reservada_por
        
    def __str__(self):
        return f"Room ID: {self.id}, Tipo: {self.tipo}, Precio: {self.precio}, Características: {self.caracteristicas}"
    
    
class Motel:
    def __init__(self, usuario: Usuario, rooms: List[Room]):
        self.usuario: Usuario = usuario
        self.rooms: list[Room] = rooms
        self.reservados: List[Tuple[int, int]] = []
        self.rooms_disponibles: List[int] = [room.id for room in rooms if room.reservada_por is None]
        
    def mostrar_rooms_disponibles(self):
        return self.rooms_disponibles
        
    def reservar_room(self, room_id: int, id_usuario: str):
        if room_id in self.rooms_disponibles and (id_usuario == self.usuario.id_user):
            self.reservados.append((room_id, self.usuario.id_user))
            self.rooms_disponibles.remove(room_id)
            print(f"Room {room_id} reservado para {self.usuario.name}")
        else:
            print(f"Room {room_id} no disponible") 
    
    def cancelar_reserva(self, room_id: int, id_usuario: str):
        if (room_id, id_usuario) in self.reservados:
            self.reservados.remove((room_id, id_usuario))
            self.rooms_disponibles.append(room_id)
            for room in self.rooms:
                if room.id == room_id:
                    room.reservada_por = None
            return print(f"Reserva de Room {room_id} cancelada para {self.usuario.name}")
        return print(f"Room {room_id} no reservado para cancelar")
        
if __name__ == "__main__":

    with open("data/datos.json", "r") as file:
        data = json.load(file)

    # Crear usuarios
    usuarios = []
    for u in data["usuarios"]:
        usuario = Usuario(
            id_user=u["id"],   # corregido
            name=u["name"],
            edad=u["edad"],
            sexo=u["sexo"],
            telefono=u["telefono"],
            email=u["email"]
        )
        usuarios.append(usuario)

    # Seleccionamos un usuario activo (ejemplo: el primero)
    usuario_activo = usuarios[0]

    # Crear motel con usuario activo
    motel = Motel(usuario_activo, rooms)

    print("Rooms disponibles inicialmente:")
    print(motel.mostrar_rooms_disponibles())

    # Reservar habitación correctamente
    motel.reservar_room(room_id=1, id_usuario=usuario_activo.id_user)

    print("Rooms disponibles después de reservar:")
    print(motel.mostrar_rooms_disponibles())
