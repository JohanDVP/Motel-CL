"""
Model representing a room reservation in the motel system.
"""

from dataclasses import dataclass


ESTADOS_VALIDOS = ("activa", "cancelada", "completada")


@dataclass
class Reserva:
    """
    Represents a room reservation made by a user.

    Attributes:
        id (int): Unique identifier of the reservation.
        id_usuario (int): ID of the user who made the reservation.
        id_room (int): ID of the reserved room.
        horas (int): Duration of the reservation in hours.
        total (float): Total cost of the reservation.
        estado (str): Current status of the reservation. Defaults to 'activa'.
    """

    id: int
    id_usuario: int
    id_room: int
    horas: int
    total: float
    estado: str = "activa"

    def __post_init__(self) -> None:
        """
        Validates all fields after initialization.

        Raises:
            ValueError: If any field contains an invalid value.
        """
        self._validar_horas()
        self._validar_total()
        self._validar_estado()

    def _validar_horas(self) -> None:
        """
        Validates that hours are greater than zero.

        Raises:
            ValueError: If hours are zero or negative.
        """
        if self.horas <= 0:
            raise ValueError(f"Las horas deben ser mayor a 0, se recibio: {self.horas}")

    def _validar_total(self) -> None:
        """
        Validates that the total cost is not negative.

        Raises:
            ValueError: If total is negative.
        """
        if self.total < 0:
            raise ValueError(f"El total no puede ser negativo: {self.total}")

    def _validar_estado(self) -> None:
        """
        Validates that the status is one of the allowed values.

        Raises:
            ValueError: If the status is not valid.
        """
        if self.estado not in ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado invalido: '{self.estado}'. "
                f"Debe ser uno de: {', '.join(ESTADOS_VALIDOS)}"
            )

    @property
    def activa(self) -> bool:
        """
        Indicates whether the reservation is currently active.

        Returns:
            bool: True if active, otherwise False.
        """
        return self.estado == "activa"