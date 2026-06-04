"""
Unit tests for verifying system custom exceptions.
"""

from src.core.exceptions import DatosInvalidosError, MotelError


def test_custom_exceptions_inheritance():
    """
    Verifica que las excepciones personalizadas hereden correctamente
    de la clase base del negocio.
    """
    error = DatosInvalidosError("El número de horas no puede ser negativo.")

    # Debe ser una instancia de sí misma y de la clase base
    assert isinstance(error, DatosInvalidosError)
    assert isinstance(error, MotelError)
    assert str(error) == "El número de horas no puede ser negativo."