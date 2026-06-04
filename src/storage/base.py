"""
Supabase client initialization base file.
"""

from supabase import Client, create_client

from src.core.config import settings


def get_supabase_client() -> Client:
    """
    Initializes and returns a Supabase client instance.
    """
    try:
        return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    except Exception as e:
        raise RuntimeError(f"Error al conectar con Supabase: {str(e)}") from e
