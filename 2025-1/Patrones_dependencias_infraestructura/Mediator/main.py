import json
from dependency import DependsOn
from network import NetworkFactoryModule
from server import ServerFactoryModule
from firewall import FirewallFactoryModule

class Mediator:
    def __init__(self, module):
        self.module = module
        self.order = []

    def _create(self, module):
        # Crear red si es necesario
        if isinstance(module, NetworkFactoryModule):
            self.order.append(module.build())
            return module.outputs()

        # Crear servidor si es necesario
        if isinstance(module, ServerFactoryModule):
            net_out = self._create(NetworkFactoryModule())
            module.depends = net_out
            self.order.append(module.build())
            return module.outputs()

        # Crear firewall si es necesario
        if isinstance(module, FirewallFactoryModule):
            srv_out = self._create(ServerFactoryModule(self._create(NetworkFactoryModule())))
            module.depends = srv_out
            self.order.append(module.build())
            return module.outputs()

        # Módulo desconocido
        self.order.append(module.build())
        return module.outputs()

    def build(self):
        # Inicia la creación con el módulo firewall
        self._create(self.module)
        merged = {"terraform": {"required_providers": {}}, "resource": {}}
        for block in self.order:
            for res_type, res_defs in block["resource"].items():
                merged_resources = merged["resource"].setdefault(res_type, {})
                merged_resources.update(res_defs)
        return merged

if __name__ == "__main__":
    mediator = Mediator(FirewallFactoryModule())
    cfg = mediator.build()
    with open("main.tf.json", "w") as f:
        json.dump(cfg, f, indent=2)
