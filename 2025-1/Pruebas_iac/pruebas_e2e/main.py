#!/usr/bin/env python3
"""
Genera configuración JSON de un servicio local, sin proveedor de nube.
"""
import json
import argparse

SERVICE_CFG_FILE = 'service_config.json'

class LocalServiceFactory:
    def __init__(self, name: str):
        self.name = name

    def build(self) -> dict:
        return {
            'resources': [
                {
                    'type': 'local_service',
                    'name': self.name,
                    'port': 0  # puerto dinámico asignado en el deploy
                }
            ]
        }

    def write(self, out_dir: str = '.'):
        cfg = self.build()
        with open(f"{out_dir}/{SERVICE_CFG_FILE}", 'w') as f:
            json.dump(cfg, f, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generar config local de servicio')
    parser.add_argument('--name', default='e2e-service', help='Nombre del servicio')
    parser.add_argument('--out', default='.', help='Directorio de salida')
    args = parser.parse_args()

    factory = LocalServiceFactory(args.name)
    factory.write(args.out)
    print(f"Archivo generado: {args.out}/{SERVICE_CFG_FILE}")
