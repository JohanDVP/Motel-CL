"""
Model representing a hotel room in the motel system.
"""

from dataclasses import dataclass, field


TIPOS_VALIDOS = ("Sencilla", "Doble", "Suite", "Jacuzzi")


@dataclass
class Room:
    """
    Represents a room in the motel.

    Attributes:
        id (int): Unique identifier of the room.
        tipo (str): Room type. Must be one of: Sencilla, Doble, Suite, Jacuzzi.
        precio (float): Price per hour of the room.
        caracteristicas (list[str]): List of room features. Defaults to empty list.
        reservada_por (int | None): ID of the user who reserved it, or None if available.
    """

    id: int
    tipo: str
    precio: float
    caracteristicas: list[str] = field(default_factory=list)
    reservada_por: int | None = None  # None = disponible

    def __post_init__(self) -> None:
        """
        Validates all fields after initialization.

        Raises:
            ValueError: If any field contains an invalid value.
        """
        self._validar_tipo()
        self._validar_precio()

    def _validar_tipo(self) -> None:
        """
        Validates that the room type is one of the allowed values.

        Raises:
            ValueError: If the room type is not valid.
        """
        if self.tipo not in TIPOS_VALIDOS:
            raise ValueError(
                f"Tipo de habitacion invalido: '{self.tipo}'. "
                f"Debe ser uno de: {', '.join(TIPOS_VALIDOS)}"
            )

    def _validar_precio(self) -> None:
        """
        Validates that the price is greater than zero.

        Raises:
            ValueError: If the price is zero or negative.
        """
        if self.precio <= 0:
            raise ValueError(f"El precio debe ser mayor a 0, se recibio: {self.precio}")

    @property
    def disponible(self) -> bool:
        """
        Indicates whether the room is available for reservation.

        Returns:
            bool: True if available, otherwise False.
        """
        return self.reservada_por is None