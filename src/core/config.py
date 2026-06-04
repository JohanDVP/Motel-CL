"""
Global application settings using Pydantic Settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # Carga automáticamente el archivo .env desde la raíz del proyecto
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )


# === REVISA QUE ESTA LÍNEA EXISTAL EN MINÚSCULAS ===
settings = Settings()