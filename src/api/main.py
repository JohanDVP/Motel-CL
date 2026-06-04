"""
Main entry point for the Motel FastAPI application.
"""

from fastapi import FastAPI
from src.api.routers import user, room, reserva

app = FastAPI(
    title="Motel Management System API",
    description="Backend relacional con arquitectura limpia conectado a Supabase.",
    version="2.0.0"
)

# Incluir los enrutadores modulares
app.include_router(user.router)
app.include_router(room.router)
app.include_router(reserva.router)


@app.get("/", tags=["Root"])
def read_root():
    return {
        "status": "online",
        "database": "connected (Supabase)",
        "docs": "/docs"
    }