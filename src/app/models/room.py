from dataclasses import dataclass, field


TIPOS_VALIDOS = ("Sencilla", "Doble", "Suite", "Jacuzzi")


@dataclass
class Room:
    """Habitacion del motel."""

    id: int
    tipo: str
    precio: float
    caracteristicas: list[str] = field(default_factory=list)
    reservada_por: int | None = None  # None = disponible

    def __post_init__(self) -> None:
        self._validar_tipo()
        self._validar_precio()

    def _validar_tipo(self) -> None:
        if self.tipo not in TIPOS_VALIDOS:
            raise ValueError(
                f"Tipo de habitacion invalido: '{self.tipo}'. "
                f"Debe ser uno de: {', '.join(TIPOS_VALIDOS)}"
            )

    def _validar_precio(self) -> None:
        if self.precio <= 0:
            raise ValueError(f"El precio debe ser mayor a 0, se recibio: {self.precio}")

    @property
    def disponible(self) -> bool:
        """Indica si la habitacion esta libre."""
        return self.reservada_por is None