"""
Módulo local para definir instancias de servidor en JSON, usa un rango IP localizado, sin proveedor cloud.
"""
import json
import ipaddress

class ServerFactoryLocal:
    def __init__(self, name: str, network_cidr: str):
        self.name = name
        self.network_cidr = network_cidr

    def _allocate_ip(self) -> str:
        net = ipaddress.IPv4Network(self.network_cidr)
        return str(list(net.hosts())[4])

    def build(self) -> dict:
        """Genera recurso de servidor en JSON local."""
        return {
            "resources": [
                {
                    "type": "local_server",
                    "name": self.name,
                    "network_ip": self._allocate_ip(),
                    "image": "ubuntu-20.04-lts",
                    "cpu": 1,
                    "memory_mb": 1024
                }
            ]
        }

    def write(self, path: str):
        with open(path, 'w') as f:
            json.dump(self.build(), f, indent=4)
