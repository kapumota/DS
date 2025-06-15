#!/usr/bin/env python3
"""
Genera configuración JSON de servidor local sin proveedor de la nube.
"""
import json
import argparse

SERVER_CFG_FILE = 'server_config.json'
class LocalServerFactory:
    def __init__(self, name: str):
        self.name = name

    def build(self) -> dict:
        # Simula definición de un servidor local
        return {
            "resources": [
                {
                    "type": "local_server",
                    "name": self.name,
                    "image": "ubuntu-20.04-lts",
                    "cpu": 2,
                    "memory_mb": 2048
                }
            ]
        }

    def write(self, path: str = '.'):
        cfg = self.build()
        with open(f"{path}/{SERVER_CFG_FILE}", 'w') as f:
            json.dump(cfg, f, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generar config local de servidor')
    parser.add_argument('--name', default='test-server', help='Nombre del servidor')
    parser.add_argument('--out', default='.', help='Directorio de salida')
    args = parser.parse_args()

    factory = LocalServerFactory(name=args.name)
    factory.write(args.out)
    print(f"Archivo generado: {args.out}/{SERVER_CFG_FILE}")
