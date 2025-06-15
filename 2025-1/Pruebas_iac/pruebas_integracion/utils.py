"""
Funciones de utilidad para simular terraform init/apply/destroy localmente.
"""
import os
import subprocess

SERVER_CFG_FILE = 'server_config.json'

def initialize() -> int:
    # Simula terraform init verificando que Python esté disponible
    return 0

def apply() -> tuple[int, bytes, bytes]:
    # Simula terraform apply creando un archivo de estado
    if not os.path.exists(SERVER_CFG_FILE):
        return 1, b'', b'Config file not found'
    # crear archivo estado
    with open('server_state.json', 'w') as f:
        f.write('applied')
    stdout = b'Apply complete! Resources: 1 added, 0 changed, 0 destroyed'
    stderr = b''
    return 0, stdout, stderr


def destroy() -> int:
    # Simula terraform destroy borrando estado generado
    if os.path.exists('server_state.json'):
        os.remove('server_state.json')
    return 0

def get_server(name: str) -> dict:
    # Simula recuperación de recurso local
    if os.path.exists('server_state.json'):
        return {"name": name, "state": "running"}
    return {"name": name, "state": "absent"}
