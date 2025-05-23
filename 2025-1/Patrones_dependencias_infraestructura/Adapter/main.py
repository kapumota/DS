import json
import access

class LocalIdentityAdapter:
    """Adapter para transformar los roles genéricos a recursos locales null_resource."""
    def __init__(self, metadata):
        self.local_users = []
        for permission, users in metadata.items():
            for user in users:
                # Mantener la misma estructura de tupla para outputs
                self.local_users.append((user, user, permission))

    def outputs(self):
        return self.local_users

class LocalProjectUsers:
    """Construye recursos null_resource para cada usuario/rol localmente."""
    def __init__(self, users):
        self._users = users
        self.resources = self._build()

    def _build(self):
        resources = []
        for (user, identity, role) in self._users:
            # Nombre único de recurso
            res_name = f"identity_{user}_{role}".replace('-', '_')
            resources.append({
                "null_resource": {
                    res_name: {
                        "triggers": {
                            "user": user,
                            "identity": identity,
                            "role": role
                        }
                    }
                }
            })
        return {"resource": resources}

if __name__ == "__main__":
    # Cargar roles genéricos
    metadata = access.Infrastructure().resources
    # Transformar a identidades locales
    users = LocalIdentityAdapter(metadata).outputs()
    # Generar configuración Terraform JSON local
    with open('main.tf.json', 'w') as outfile:
        json.dump(LocalProjectUsers(users).resources,
                  outfile, sort_keys=True, indent=4)
