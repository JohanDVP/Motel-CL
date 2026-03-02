class DatosIncorrectos(Exception): #datos incorrectos
    pass

class UsuarioNoEncontradoError(Exception): #Si no existe el user
    pass

class RoomNoEncontradaError(Exception): #Si no se encuentra el id de la habitacion
    pass

class RoomNoDisponibleError(Exception): # Si la habitacionque intenta tomar ya esta ocupada
    pass

class ReservaNoEncontradaError(Exception): #Si no existe una reserva con ese id
    pass


