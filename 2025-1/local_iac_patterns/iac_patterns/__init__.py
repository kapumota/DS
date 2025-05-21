"""Paquete iac_patterns

Una colección de implementaciones de patrones de diseño (Singleton, Factory,
Prototype, Builder, Composite) adaptadas para generar configuraciones JSON de Terraform
que funcionan únicamente de forma local. Todos los recursos generados dependen
únicamente de los proveedores `null_resource` y `local_file`, por lo tanto, **no**
se requiere ningún proveedor en la nube, demonio de Docker o hipervisor externo.

Ejemplo de uso
--------------
```python
from iac_patterns.builder import InfrastructureBuilder

builder = InfrastructureBuilder(env_name="demo")
builder.build_null_fleet(count=3)
builder.export(path="terraform/main.tf.json")
"""

from .singleton import ConfigSingleton
from .factory import NullResourceFactory
from .prototype import ResourcePrototype
from .composite import CompositeModule
from .builder import InfrastructureBuilder

__all__ = [
    "ConfigSingleton",
    "NullResourceFactory",
    "ResourcePrototype",
    "CompositeModule",
    "InfrastructureBuilder",
]
