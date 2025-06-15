"""
Módulo local para definir una red en JSON, sin dependencia de proveedores de la nube.
"""
import json
import netaddr

class NetworkFactoryLocal:
    def __init__(self, name: str, ip_range: str):
        self.name = name
        self.network = f"{name}-net"
        self.ip_range = ip_range

    def build(self) -> dict:
        """Genera recursos de red en formato JSON local."""
        net = netaddr.IPNetwork(self.ip_range)
        return {
            "resources": [
                {
                    "type": "local_network",
                    "name": self.network,
                    "cidr": str(net)
                }
            ]
        }

    def write(self, path: str):
        with open(path, 'w') as f:
            json.dump(self.build(), f, indent=4)
