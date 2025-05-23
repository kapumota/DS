from dependency import DependsOn

class NetworkFactoryModule:
    def build(self):
        return {
            "resource": {
                "null_resource": {
                    "network": {
                        "triggers": {
                            "name": "hello-world-network"
                        }
                    }
                }
            }
        }

    def outputs(self):
        return DependsOn("null_resource", "network", {"name": "hello-world-network"})
