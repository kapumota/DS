"""
Prueba E2E local: desde la generación hasta la respuesta HTTP.
"""
import os
import pytest
import requests
from pruebas_e2e.main import LocalServiceFactory, SERVICE_CFG_FILE
import pruebas_e2e.utils as utils

TEST_NAME = 'hello-world-e2e'

@ pytest.fixture()
def e2e_flow(tmp_path, monkeypatch):
    d = tmp_path
    monkeypatch.chdir(d)
    # generar config
    LocalServiceFactory(TEST_NAME).write('.')
    assert os.path.exists(SERVICE_CFG_FILE)
    # init
    assert utils.initialize() == 0
    # deploy
    code, url, err = utils.apply()
    assert code == 0 and err == b''
    yield url
    # teardown
    assert utils.destroy() == 0

def test_e2e_service_response(e2e_flow):
    url = e2e_flow
    resp = requests.get(url)
    assert resp.status_code == 200
    assert "Esta corriendo!" in resp.text
