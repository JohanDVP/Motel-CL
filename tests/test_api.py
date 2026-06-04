"""
Integration tests for the FastAPI application layer.
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_api_docs_endpoint_is_available():
    """
    Verifica que la documentación interactiva de Swagger (OpenAPI)
    esté configurada y responda exitosamente.
    """
    respuesta = client.get("/docs")
    assert respuesta.status_code == 200
    assert "swagger-ui" in respuesta.text.lower()


def test_api_redoc_endpoint_is_available():
    """
    Verifica que la interfaz de documentación alterna ReDoc
    esté disponible para los evaluadores.
    """
    respuesta = client.get("/redoc")
    assert respuesta.status_code == 200