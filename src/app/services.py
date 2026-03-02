# src/app/services.py

from .models import Habitacion, Cliente, Reserva
from .storage import HabitacionStorage, ClienteStorage, ReservaStorage
from .exceptions import (
    HabitacionNoDisponibleError,
    HabitacionNoEncontradaError,
    ClienteNoEncontradoError,
    ReservaNoEncontradaError,
    DatosInvalidosError,
)


class HabitacionService:

    def __init__(self, storage: HabitacionStorage) -> None:
        self._storage = storage

    def listar(self) -> list[Habitacion]:
        return self._storage.obtener_todas()

    def listar_disponibles(self) -> list[Habitacion]:
        return [h for h in self._storage.obtener_todas() if h.disponible]

    def buscar(self, id: int) -> Habitacion:
        for h in self._storage.obtener_todas():
            if h.id == id:
                return h
        raise HabitacionNoEncontradaError(f"No existe habitación con ID {id}")

    def agregar(self, habitacion: Habitacion) -> None:
        if habitacion.precio_por_hora <= 0:
            raise DatosInvalidosError("El precio debe ser mayor a 0")
        if not habitacion.tipo.strip():
            raise DatosInvalidosError("El tipo de habitación no puede estar vacío")
        self._storage.guardar(habitacion)


class ClienteService:

    def __init__(self, storage: ClienteStorage) -> None:
        self._storage = storage

    def listar(self) -> list[Cliente]:
        return self._storage.obtener_todos()

    def buscar(self, id: int) -> Cliente:
        for c in self._storage.obtener_todos():
            if c.id == id:
                return c
        raise ClienteNoEncontradoError(f"No existe cliente con ID {id}")

    def registrar(self, cliente: Cliente) -> None:
        if not cliente.email or "@" not in cliente.email:
            raise DatosInvalidosError("El email no es válido")
        if not cliente.telefono.strip():
            raise DatosInvalidosError("El teléfono no puede estar vacío")
        self._storage.guardar(cliente)


class ReservaService:
   

    def __init__(
        self,
        reserva_storage: ReservaStorage,
        habitacion_service: HabitacionService,
        cliente_service: ClienteService,
    ) -> None:

        self._storage = reserva_storage
        self._habitaciones = habitacion_service
        self._clientes = cliente_service

    def crear(self, cliente_id: int, habitacion_id: int, horas: int) -> Reserva:
        
        if horas <= 0:
            raise DatosInvalidosError("Las horas deben ser mayor a 0")

        cliente = self._clientes.buscar(cliente_id)  
        habitacion = self._habitaciones.buscar(habitacion_id)  

        if not habitacion.disponible:
            raise HabitacionNoDisponibleError(
                f"La habitación {habitacion_id} no está disponible"
            )

        total = habitacion.precio_por_hora * horas
        reservas = self._storage.obtener_todas()
        nuevo_id = max((r.id for r in reservas), default=0) + 1

        reserva = Reserva(
            id=nuevo_id,
            cliente_id=cliente.id,
            habitacion_id=habitacion.id,
            horas=horas,
            total=total,
        )

        habitacion.disponible = False
        self._habitaciones._storage.guardar(habitacion)
        self._storage.guardar(reserva)
        return reserva

    def cancelar(self, reserva_id: int) -> None:
        for reserva in self._storage.obtener_todas():
            if reserva.id == reserva_id:
                if reserva.estado != "activa":
                    raise DatosInvalidosError("Solo se pueden cancelar reservas activas")
                reserva.estado = "cancelada"
                habitacion = self._habitaciones.buscar(reserva.habitacion_id)
                habitacion.disponible = True
                self._habitaciones._storage.guardar(habitacion)
                self._storage.guardar(reserva)
                return
        raise ReservaNoEncontradaError(f"No existe reserva con ID {reserva_id}")

    def listar(self) -> list[Reserva]:
        return self._storage.obtener_todas()