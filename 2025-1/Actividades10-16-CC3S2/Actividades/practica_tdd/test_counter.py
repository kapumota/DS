"""
test_counter.py
Contiene las pruebas de Pytest para el servicio 'counter'.
"""
import pytest
from counter import app, COUNTERS
from http import HTTPStatus

@pytest.fixture(autouse=True)
def clean_counters():
    """
    Fixture que limpia el diccionario de contadores (COUNTERS) 
    antes de cada prueba. De esta forma, cada test inicia en 
    un estado limpio y no interfiere con los demás.
    """
    COUNTERS.clear()


@pytest.fixture
def client():
    """
    Configura un cliente de pruebas de Flask.
    Esto permite hacer requests a la app sin levantar un servidor real.
    """
    return app.test_client()


def test_create_a_counter(client):
    """Debe crear un contador y retornar 201 CREATED."""
    response = client.post("/counters/test_counter")
    assert response.status_code == HTTPStatus.CREATED

    data = response.get_json()
    assert "test_counter" in data
    assert data["test_counter"] == 0


def test_duplicate_counter(client):
    """Debe devolver 409 CONFLICT al intentar crear un contador duplicado."""
    # Crear por primera vez
    response = client.post("/counters/test_counter")
    assert response.status_code == HTTPStatus.CREATED

    # Intentar crear el mismo contador nuevamente
    response = client.post("/counters/test_counter")
    assert response.status_code == HTTPStatus.CONFLICT


def test_update_counter(client):
    """Debe actualizar (incrementar) el contador con PUT y retornar 200 OK."""
    # 1. Crear un contador
    response = client.post("/counters/update_me")
    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()
    assert data["update_me"] == 0

    # 2. Actualizar el contador
    response = client.put("/counters/update_me")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    # Asumimos que incrementa de 0 a 1
    assert data["update_me"] == 1


def test_read_counter(client):
    """Debe leer un contador con GET y retornar 200 OK."""
    # 1. Crear un contador
    response = client.post("/counters/read_me")
    assert response.status_code == HTTPStatus.CREATED

    # 2. Leer el contador
    response = client.get("/counters/read_me")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    # Debería estar en 0 justo después de crearlo
    assert data["read_me"] == 0


def test_delete_counter(client):
    """Debe eliminar un contador con DELETE y retornar 204 NO CONTENT."""
    # 1. Crear un contador
    response = client.post("/counters/delete_me")
    assert response.status_code == HTTPStatus.CREATED

    # 2. Eliminar el contador
    response = client.delete("/counters/delete_me")
    assert response.status_code == HTTPStatus.NO_CONTENT

    # 3. Verificar que ya no existe
    response = client.get("/counters/delete_me")
    assert response.status_code == HTTPStatus.NOT_FOUND

