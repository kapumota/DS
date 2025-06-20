"""
Suite de integración para los endpoints de ítems.

Se asume que la lógica de negocio está en microservice/main.py y que
FastAPI registra las rutas en /api/items.
"""

import pytest
from fastapi.testclient import TestClient
from microservice.main import app

# Fixtures

@pytest.fixture(scope="module")
def client():
    """Cliente síncrono sobre la app ASGI (Starlette+FastAPI)."""
    with TestClient(app) as c:
        yield c

# Casos de prueba

ITEM_NAME = "test-item"
ITEM_DESCRIPTION = "Descripción de prueba"


def test_healthcheck_items_endpoint(client):
    """El listado debería responder 200 OK aun cuando no haya ítems."""
    resp = client.get("/api/items")
    assert resp.status_code == 200


def test_create_item_and_verify_in_list(client):
    """
    1) Crea un ítem          -> 201 Created
    2) Devuelve los datos    -> nombre y descripción coinciden
    3) El ítem aparece luego en el listado general
    """
    payload = {"name": ITEM_NAME, "description": ITEM_DESCRIPTION}
    create_resp = client.post("/api/items", json=payload)
    assert create_resp.status_code == 201

    created = create_resp.json()
    assert created["name"] == ITEM_NAME
    assert created["description"] == ITEM_DESCRIPTION

    list_resp = client.get("/api/items")
    assert list_resp.status_code == 200
    items = list_resp.json()

    assert any(i["name"] == ITEM_NAME for i in items), (
        f"El ítem '{ITEM_NAME}' debería figurar en la lista"
    )
