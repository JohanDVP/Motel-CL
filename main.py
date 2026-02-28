import json
from typing import List

class Usuario:
    def __init__(self, name: str, edad: int, sexo: str, telefono: str, email: str):
        self.name: str = name
        self.edad: int = edad
        self.sexo: str = sexo
        self.telefono: str = telefono
        self.email: str = email
        
class Room:
    def __init__(self, id: int, tipo: str, precio: float, caracteristicas: List[str]):
        self.id: int = id
        self.tipo: str = tipo
        self.precio: float = precio
        self.caracteristicas: List[str] = caracteristicas
        
    def __str__(self):
        return f"Room ID: {self.id}, Tipo: {self.tipo}, Precio: {self.precio}, Características: {self.caracteristicas}"
    
class Motel:
    def __init__(self, usuario: Usuario, rooms: List[Room]):
        self.usuario: Usuario = usuario
        self.rooms: list[Room] = rooms
        
    def reservar_room(self, room_id: int):
        for room in self.rooms:
            if room.id == room_id:
                print(f"Room {room_id} reservado para {self.usuario.name}")
                return
        print(f"Room {room_id} no disponible") 
        
        
if __name__ == "__main__":
    with open("datos.json", "r") as file:
        data = json.load(file)
        
    usuario = Usuario(
        name=data["usuario"]["name"],
        edad=data["usuario"]["edad"],
        sexo=data["usuario"]["sexo"],
        telefono=data["usuario"]["telefono"],
        email=data["usuario"]["email"]
    )
    
    room = Room(
        id=data["rooms"][0]["id"],
        tipo=data["rooms"][0]["tipo"],
        precio=data["rooms"][0]["precio"],
        caracteristicas=data["rooms"][0]["caracteristicas"]
    )
    
    
    motel = Motel(usuario=usuario, rooms=[room])
    
    print(f"Usuario: {motel.usuario.name}, Edad: {motel.usuario.edad}, Sexo: {motel.usuario.sexo}, Telefono: {motel.usuario.telefono}, Email: {motel.usuario.email}")
    
usuarios = Usuario(name="Maria", edad=30, sexo="Femenino", telefono="1234567890", email="maria@example.com")
room1 = Room(id=1, tipo="Sencilla", precio=50.0, caracteristicas=["Cama individual", "Baño privado"])
room2 = Room(id=2, tipo="Doble", precio=80.0, caracteristicas=["Cama matrimonial", "Baño privado", "TV"])
print(room1)
