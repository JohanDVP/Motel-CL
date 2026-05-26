from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import users, rooms, reservas

app = FastAPI(title="Motelandro API")

# <-- COPIA Y PEGA ESTO JUSTO AQUÍ:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Le da permiso a tu página web de conectarse
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(reservas.router)