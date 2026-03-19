from dataclasses import dataclass


ESTADOS_VALIDOS = ("activa", "cancelada", "completada")


@dataclass
class Reserva:
    """Reserva de una habitacion por un cliente."""

    id: int
    id_usuario: int
    id_room: int
    horas: int
    total: float
    estado: str = "activa"

    def __post_init__(self) -> None:
        self._validar_horas()
        self._validar_total()
        self._validar_estado()

    def _validar_horas(self) -> None:
        if self.horas <= 0:
            raise ValueError(f"Las horas deben ser mayor a 0, se recibio: {self.horas}")

    def _validar_total(self) -> None:
        if self.total < 0:
            raise ValueError(f"El total no puede ser negativo: {self.total}")

    def _validar_estado(self) -> None:
        if self.estado not in ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado invalido: '{self.estado}'. "
                f"Debe ser uno de: {', '.join(ESTADOS_VALIDOS)}"
            )

    @property
    def activa(self) -> bool:
        """Indica si la reserva esta activa."""
        return self.estado == "activa"