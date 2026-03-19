from dataclasses import dataclass


@dataclass
class Usuario:
    """Cliente del motel."""

    id_user: int
    name: str
    edad: int
    sexo: str
    telefono: str
    email: str

    def __post_init__(self) -> None:
        self._validar_email()
        self._validar_telefono()
        self._validar_edad()
        self._validar_sexo()

    def _validar_email(self) -> None:
        if "@" not in self.email or "." not in self.email.split("@")[-1]:
            raise ValueError(f"Email invalido: '{self.email}'")

    def _validar_telefono(self) -> None:
        if not self.telefono.strip():
            raise ValueError("El telefono no puede estar vacio")

    def _validar_edad(self) -> None:
        if self.edad < 18:
            raise ValueError("El usuario debe ser mayor de edad")

    def _validar_sexo(self) -> None:
        if self.sexo not in ("M", "F", "Otro"):
            raise ValueError(f"Sexo invalido: '{self.sexo}'. Debe ser M, F u Otro")