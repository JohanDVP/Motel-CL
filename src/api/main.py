from fastapi import FastAPI
from api.routers import users, rooms, reservas

app = FastAPI(title="Motelandro API")

app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(reservas.router)