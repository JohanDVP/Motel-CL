"""
Model representing a motel client in the system.
"""

from dataclasses import dataclass


@dataclass
class Usuario:
    """
    Represents a client of the motel.

    Attributes:
        id_user (int): Unique identifier of the user.
        name (str): Full name of the user.
        edad (int): Age of the user. Must be 18 or older.
        sexo (str): Gender of the user. Must be 'M', 'F' or 'Otro'.
        telefono (str): Contact phone number. Cannot be empty.
        email (str): Email address. Must contain '@' and a valid domain.
    """

    id_user: int
    name: str
    edad: int
    sexo: str
    telefono: str
    email: str

    def __post_init__(self) -> None:
        """
        Validates all fields after initialization.

        Raises:
            ValueError: If any field contains an invalid value.
        """
        self._validar_email()
        self._validar_telefono()
        self._validar_edad()
        self._validar_sexo()

    def _validar_email(self) -> None:
        """
        Validates that the email contains '@' and a valid domain.

        Raises:
            ValueError: If the email format is invalid.
        """
        if "@" not in self.email or "." not in self.email.split("@")[-1]:
            raise ValueError(f"Email invalido: '{self.email}'")

    def _validar_telefono(self) -> None:
        """
        Validates that the phone number is not empty.

        Raises:
            ValueError: If the phone number is empty or blank.
        """
        if not self.telefono.strip():
            raise ValueError("El telefono no puede estar vacio")

    def _validar_edad(self) -> None:
        """
        Validates that the user is at least 18 years old.

        Raises:
            ValueError: If the user is under 18.
        """
        if self.edad < 18:
            raise ValueError("El usuario debe ser mayor de edad")

    def _validar_sexo(self) -> None:
        """
        Validates that the gender is one of the allowed values.

        Raises:
            ValueError: If the gender value is not valid.
        """
        if self.sexo not in ("M", "F", "Otro"):
            raise ValueError(f"Sexo invalido: '{self.sexo}'. Debe ser M, F u Otro")