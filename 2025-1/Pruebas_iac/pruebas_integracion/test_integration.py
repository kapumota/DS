import os
import pytest
from pruebas_integracion.main import LocalServerFactory, SERVER_CFG_FILE
import pruebas_integracion.utils as utils

TEST_NAME = 'hello-world'

@ pytest.fixture()
def apply_changes(tmp_path, monkeypatch):
    # Prepara directorio de trabajo
    d = tmp_path
    monkeypatch.chdir(str(d))
    # Genera configuración
    LocalServerFactory(TEST_NAME).write('.')
    assert os.path.exists(SERVER_CFG_FILE)
    # Simula init
    assert utils.initialize() == 0
    # Aplica cambios
    result = utils.apply()
    yield result
    # Destruye recursos simulados
    assert utils.destroy() == 0

def test_return_code(apply_changes):
    return_code, stdout, stderr = apply_changes
    assert return_code == 0

def test_no_errors(apply_changes):
    _, _, stderr = apply_changes
    assert stderr == b''

def test_resource_added(apply_changes):
    _, stdout, _ = apply_changes
    assert b'Resources: 1 added' in stdout

def test_server_running(apply_changes):
    server = utils.get_server(TEST_NAME)
    assert server['state'] == 'running'
