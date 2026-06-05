"""
Integration tests for the FastAPI application layer.
"""

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

def test_listar_reservas_endpoint():
    # Esto probará la ruta GET /reservas/
    response = client.get("/reservas/")
    # Si te da 200, excelente. 
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_reserva_invalid_endpoint():
    # Esto prueba que el endpoint maneja mal los datos (prueba de robustez)
    response = client.post("/reservas/", json={"invalid": "data"})
    assert response.status_code == 422 # Código de error de validación de Pydantic