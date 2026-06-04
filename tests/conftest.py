import os

import pytest


@pytest.fixture(autouse=True)
def mock_env_vars():
    """Establece variables de entorno falsas para los tests."""
    os.environ["SUPABASE_URL"] = "https://mock.url"
    os.environ["SUPABASE_KEY"] = "mock-key"