import json

def hello_server_local(name, network):
    return {
        "resource": [
            {
                "null_resource": [
                    {
                        "hello-server": [
                            {
                                "triggers": {
                                    "name": name,
                                    "network": network
                                },
                                "provisioner": [
                                    {
                                        "local-exec": {
                                            "command": f"echo 'Arrancando servidor {name} en red {network}'"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

if __name__ == "__main__":
    # Estos valores podrían leerse de variables de entorno o argumentos.
    name = "hello-world"
    network = "local-network"

    config = hello_server_local(name=name, network=network)
    with open('main.tf.json', 'w') as outfile:
        json.dump(config, outfile, sort_keys=True, indent=4)
