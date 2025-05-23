from dependency import DependsOn

class FirewallFactoryModule:
    def __init__(self, depends=None):
        self.depends = depends

    def build(self):
        triggers = {"port": "22"}
        if self.depends:
            triggers["depends_on"] = f"{self.depends.resource_type}.{self.depends.resource_id}"
        return {
            "resource": {
                "null_resource": {
                    "firewall": {"triggers": triggers}
                }
            }
        }

    def outputs(self):
        return DependsOn("null_resource", "firewall", {"port": "22"})
