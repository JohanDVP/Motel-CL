"""
Global custom exceptions for the Motel Management System.
"""


class MotelError(Exception):
    """Excepción base para todos los errores del negocio del motel."""

    pass


class UsuarioNoEncontradoError(MotelError):
    """Se dispara cuando un cliente no existe en Supabase."""

    pass


class RoomNoEncontradaError(MotelError):
    """Se dispara cuando una habitación no existe en el inventario."""

    pass


class RoomNoDisponibleError(MotelError):
    """Se dispara si intentan reservar una habitación ya ocupada."""

    pass


class ReservaNoEncontradaError(MotelError):
    """Se dispara cuando se busca un ID de reserva inexistente."""

    pass


class DatosInvalidosError(MotelError):
    """Se dispara si las reglas de negocio financieras o de tiempo fallan."""

    pass
