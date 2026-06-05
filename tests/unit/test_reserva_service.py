import pytest
from unittest.mock import MagicMock
from src.services.reservation_service import ReservaService
from src.core.exceptions import RoomNoDisponibleError, ReservaNoEncontradaError
from src.schemas.reserva import ReservaCreate

@pytest.fixture
def service():
    # Creamos los mocks de las dependencias
    mock_repo = MagicMock()
    mock_room_svc = MagicMock()
    mock_user_svc = MagicMock()
    return ReservaService(mock_repo, mock_room_svc, mock_user_svc), mock_repo, mock_room_svc, mock_user_svc

def test_crear_reserva_exitoso(service):
    res_svc, repo, room_svc, user_svc = service
    
    # Configuramos el comportamiento esperado de los mocks
    user_svc.buscar.return_value = MagicMock(id_user=1)
    room_svc.buscar.return_value = MagicMock(id=10, precio=50, reservada_por=None)
    repo.create.return_value = MagicMock()

    cmd = ReservaCreate(id_usuario=1, id_room=10, horas=2)
    res_svc.crear(cmd)

    # Verificamos que se llamó a la base de datos y se marcó la habitación
    repo.create.assert_called_once()
    room_svc.marcar_como_ocupada.assert_called_once_with(10, 1)

def test_crear_reserva_habitacion_ocupada(service):
    res_svc, repo, room_svc, user_svc = service
    
    user_svc.buscar.return_value = MagicMock(id_user=1)
    # Simulamos que la habitación YA está reservada
    room_svc.buscar.return_value = MagicMock(id=10, reservada_por=99)

    cmd = ReservaCreate(id_usuario=1, id_room=10, horas=2)
    
    with pytest.raises(RoomNoDisponibleError):
        res_svc.crear(cmd)

def test_cancelar_reserva_no_existe(service):
    res_svc, repo, _, _ = service
    repo.get_by_id.return_value = None # Simulamos que no existe

    with pytest.raises(ReservaNoEncontradaError):
        res_svc.cancelar(999)

def test_eliminar_reserva(service):
    res_svc, repo, room_svc, _ = service
    # Simulamos que existe
    repo.get_by_id.return_value = MagicMock(id=1, estado="activa", id_room=10)
    
    res_svc.eliminar(1)
    
    # Verificamos que se liberó la habitación y se borró del repo
    room_svc.liberar_habitacion.assert_called_once_with(10)
    repo.delete.assert_called_once_with(1)