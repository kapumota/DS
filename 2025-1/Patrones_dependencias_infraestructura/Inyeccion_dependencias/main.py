import ipaddress
import json

def get_network_metadata(path="network/network_metadata.json"):
    with open(path) as f:
        data = json.load(f)
    return data['name'], data['cidr']

class ServerFactoryModule:
    def __init__(self, name, metadata_path="network/network_metadata.json"):
        self._name = name
        network_name, cidr = get_network_metadata(metadata_path)
        self._network = network_name
        self._network_ip = self._allocate_fifth_ip_address_in_range(cidr)
        self.resources = self._build()

    def _allocate_fifth_ip_address_in_range(self, ip_range):
        network = ipaddress.IPv4Network(ip_range)
        return str(list(network.hosts())[4])

    def _build(self):
        return {
            "resource": {
                "null_resource": {
                    "server": {
                        "triggers": {
                            "name": self._name,
                            "subnetwork": self._network,
                            "network_ip": self._network_ip
                        },
                        "provisioner": [{
                            "local-exec": {
                                "command": (
                                    f"echo Server {self._name} \n"
                                    f"  usa red: {self._network} \n"
                                    f"  IP asignada: {self._network_ip}"
                                )
                            }
                        }]
                    }
                }
            }
        }

if __name__ == "__main__":
    server = ServerFactoryModule(name="hello-world")
    with open('server.tf.json', 'w') as f:
        json.dump(server.resources, f, sort_keys=True, indent=4)
