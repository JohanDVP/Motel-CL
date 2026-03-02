"""Menu principal del motel."""

import typer
from rich.console import Console
from rich.table import Table
from src.app.storage import UsuarioStorage, RoomStorage, ReservaStorage
from src.app.services import UsuarioService, RoomService, ReservaService
from src.app.models import Usuario
from src.app.exceptions import RoomNoDisponibleError, RoomNoEncontradaError, UsuarioNoEncontradoError, ReservaNoEncontradaError, DatosInvalidosError

app = typer.Typer(help="Motelandro - Sistema de reservas")
console = Console()

_usr = UsuarioService(UsuarioStorage())
_rooms = RoomService(RoomStorage())
_res = ReservaService(ReservaStorage(), _rooms, _usr)


@app.command()
def ver_rooms() -> None:
    """Ver todas las habitaciones."""
    tabla = Table(title="Habitaciones")
    tabla.add_column("ID", style="cyan")
    tabla.add_column("Tipo", style="magenta")
    tabla.add_column("Precio", style="green")
    tabla.add_column("Estado", style="yellow")
    for r in _rooms.listar():
        estado = "Disponible" if r.reservada_por is None else f"Ocupada"
        tabla.add_row(str(r.id), r.tipo, f"${r.precio}", estado)
    console.print(tabla)


@app.command()
def registrar_usuario(
    nombre: str = typer.Option(..., prompt=True),
    edad: int = typer.Option(..., prompt=True),
    sexo: str = typer.Option(..., prompt=True),
    telefono: str = typer.Option(..., prompt=True),
    email: str = typer.Option(..., prompt=True),) -> None:

    """Registrar un usuario nuevo."""
    nuevo_id = max((u.id_user for u in _usr.listar()), default=0) + 1
    try:
        _usr.registrar(Usuario(id_user=nuevo_id, name=nombre, edad=edad, sexo=sexo, telefono=telefono, email=email))
        console.print(f"[green]Usuario {nombre} registrado![/green]")
    except DatosInvalidosError as e:
        console.print(f"[red]Error: {e}[/red]")


@app.command()
def reservar(
    id_usuario: int = typer.Option(..., prompt="ID del usuario"),
    id_room: int = typer.Option(..., prompt="ID de la habitacion"),
    horas: int = typer.Option(..., prompt="Cuantas horas"),) -> None:
    """Reservar una habitacion."""
    try:
        r = _res.crear(id_usuario, id_room, horas)
        console.print(f"[green]Reserva creada! Total: ${r.total}[/green]")
    except (RoomNoDisponibleError, RoomNoEncontradaError, UsuarioNoEncontradoError, DatosInvalidosError) as e:
        console.print(f"[red]Error: {e}[/red]")


@app.command()
def cancelar_reserva(
    reserva_id: int = typer.Option(..., prompt="ID de la reserva"),) -> None:
    """Cancelar una reserva."""
    try:
        _res.cancelar(reserva_id)
        console.print(f"[yellow]Reserva {reserva_id} cancelada[/yellow]")
    except (ReservaNoEncontradaError, DatosInvalidosError) as e:
        console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    app()