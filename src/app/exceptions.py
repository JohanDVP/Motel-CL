class RoomNoDisponibleError(Exception):
    """Se lanza cuando se intenta reservar una habitacion ya ocupada."""


class RoomNoEncontradaError(Exception):
    """Se lanza cuando no existe una habitacion con el ID dado."""


class UsuarioNoEncontradoError(Exception):
    """Se lanza cuando no existe un usuario con el ID dado."""


class ReservaNoEncontradaError(Exception):
    """Se lanza cuando no existe una reserva con el ID dado."""


class DatosInvalidosError(Exception):
    """Se lanza cuando los datos proporcionados son invalidos."""