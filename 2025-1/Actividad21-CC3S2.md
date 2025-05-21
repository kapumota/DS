### Actividad: Patrones para módulos de infraestructura

En esta actividad: 
1. Profundizaremos en los patrones **Singleton**, **Factory**, **Prototype**, **Composite** y **Builder** aplicados a IaC.
2. Analizaremos y extenderemos el código Python existente para generar configuraciones Terraform locales.
3. Diseñaremos soluciones propias, escribir tests y evaluar escalabilidad.


#### Fase 0: Preparación
Utiliza para esta actividad el siguiente [proyecto](https://github.com/kapumota/DS/tree/main/2025-1/local_iac_patterns) como referencia.

1. **Configura** el entorno virtual:

   ```bash
   cd local_iac_patterns
   python -m venv .venv && source .venv/bin/activate
   pip install --upgrade pip
   ```
2. **Genera** la infraestructura base y valida:

   ```bash
   python generate_infra.py
   cd terraform
   terraform init
   terraform validate
   ```
3. **Inspecciona** `terraform/main.tf.json` para ver los bloques `null_resource` generados.


#### Fase 1: Exploración y análisis

Para cada patrón, localiza el archivo correspondiente y responde (los códigos son de referencia):

##### 1. Singleton

```python
# singleton.py
import threading
from datetime import datetime

class SingletonMeta(type):
    _instances: dict = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class ConfigSingleton(metaclass=SingletonMeta):
    def __init__(self, env_name: str):
        self.env_name = env_name
        self.settings: dict = {}
        self.created_at: str = datetime.utcnow().isoformat()
```

* **Tarea**: Explica cómo `SingletonMeta` garantiza una sola instancia y el rol del `lock`.

#### 2. Factory

```python
# factory.py
import uuid
from datetime import datetime

class NullResourceFactory:
    @staticmethod
    def create(name: str, triggers: dict = None) -> dict:
        triggers = triggers or {
            "factory_uuid": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat()
        }
        return {
            "resource": {
                "null_resource": {
                    name: {"triggers": triggers}
                }
            }
        }
```

* **Tarea**: Detalla cómo la fábrica encapsula la creación de `null_resource` y el propósito de sus `triggers`.

#### 3. Prototype

```python
# prototype.py
from copy import deepcopy
from typing import Callable

class ResourcePrototype:
    def __init__(self, template: dict):
        self.template = template

    def clone(self, mutator: Callable[[dict], None]) -> dict:
        new_copy = deepcopy(self.template)
        mutator(new_copy)
        return new_copy
```

* **Tarea**: Dibuja un diagrama UML del proceso de clonación profunda y explica cómo el **mutator** permite personalizar cada instancia.

#### 4. Composite

```python
# composite.py
from typing import List, Dict

class CompositeModule:
    def __init__(self):
        self.children: List[Dict] = []

    def add(self, block: Dict):
        self.children.append(block)

    def export(self) -> Dict:
        merged: Dict = {"resource": {}}
        for child in self.children:
            # Imagina que unimos dicts de forma recursiva
            for rtype, resources in child["resource"].items():
                merged["resource"].setdefault(rtype, {}).update(resources)
        return merged
```

* **Tarea**: Describe cómo `CompositeModule` agrupa múltiples bloques en un solo JSON válido para Terraform.

#### 5. Builder

```python
# builder.py
import json
from composite import CompositeModule
from factory import NullResourceFactory
from prototype import ResourcePrototype

class InfrastructureBuilder:
    def __init__(self):
        self.module = CompositeModule()

    def build_null_fleet(self, count: int):
        base = NullResourceFactory.create("app")
        proto = ResourcePrototype(base)
        for i in range(count):
            def mutator(block):
                # Renombrar recurso "app" a "app_<i>"
                res = block["resource"]["null_resource"].pop("app")
                block["resource"]["null_resource"][f"app_{i}"] = res
            self.module.add(proto.clone(mutator))
        return self

    def export(self, path: str = "terraform/main.tf.json"):
        with open(path, "w") as f:
            json.dump(self.module.export(), f, indent=2)
```

* **Tarea**: Explica cómo `InfrastructureBuilder` orquesta Factory -> Prototype -> Composite y genera el archivo JSON final.

> **Entregable fase 1**: Documentocon fragmentos de código destacados, explicación de cada patrón y un diagrama UML simplificado.


#### Fase 2: Ejercicios prácticos 

Extiende el código base en una rama nueva por ejercicio:

#### Ejercicio 2.1: Extensión del Singleton

* **Objetivo**: Añadir un método `reset()` que limpie `settings` pero mantenga `created_at`.
* **Código de partida**:

  ```python
  class ConfigSingleton(metaclass=SingletonMeta):
      # ...
      def reset(self):
          # TODO: implementar
  ```
* **Validación**:

  ```python
  c1 = ConfigSingleton("dev")
  created = c1.created_at
  c1.settings["x"] = 1
  c1.reset()
  assert c1.settings == {}
  assert c1.created_at == created
  ```

#### Ejercicio 2.2: Variación de la Factory

* **Objetivo**: Crear `TimestampedNullResourceFactory` que acepte un `fmt: str`.
* **Esqueleto**:

  ```python
  class TimestampedNullResourceFactory(NullResourceFactory):
      @staticmethod
      def create(name: str, fmt: str) -> dict:
          ts = datetime.utcnow().strftime(fmt)
          # TODO: usar ts en triggers
  ```
* **Prueba**: Genera recurso con formato `'%Y%m%d'` y aplica `terraform plan`.

#### Ejercicio 2.3: Mutaciones avanzadas con Prototype

* **Objetivo**: Clonar un prototipo y, en el mutator, añadir un bloque `local_file`.
* **Referencia**:

  ```python
  def add_welcome_file(block: dict):
      block["resource"]["null_resource"]["app_0"]["triggers"]["welcome"] = "¡Hola!"
      block["resource"]["local_file"] = {
          "welcome_txt": {
              "content": "Bienvenido",
              "filename": "${path.module}/bienvenida.txt"
          }
      }
  ```
* **Resultado**: Al `terraform apply`, genera `bienvenida.txt`.

#### Ejercicio 2.4: Submódulos con Composite

* **Objetivo**: Modificar `CompositeModule.add()` para soportar submódulos:

  ```python
  # composite.py (modificado)
  def export(self):
      merged = {"module": {}, "resource": {}}
      for child in self.children:
          if "module" in child:
              merged["module"].update(child["module"])
          # ...
  ```
* **Tarea**: Crea dos submódulos "network" y "app" en la misma export y valida con Terraform.

#### Ejercicio 2.5: Builder personalizado

* **Objetivo**: En `InfrastructureBuilder`, implementar `build_group(name: str, size: int)`:

  ```python
  def build_group(self, name: str, size: int):
      base = NullResourceFactory.create(name)
      proto = ResourcePrototype(base)
      group = CompositeModule()
      for i in range(size):
          def mut(block):  # renombrar
              res = block["resource"]["null_resource"].pop(name)
              block["resource"]["null_resource"][f"{name}_{i}"] = res
          group.add(proto.clone(mut))
      self.module.add({"module": {name: group.export()}})
      return self
  ```
* **Validación**: Exportar a JSON y revisar anidamiento `module -> <name> -> resource`.

> **Entregable Fase 2**: Ramas Git con cada ejercicio, código modificado y logs de `terraform plan`/`apply`.


#### Fase 3: Desafíos teórico-prácticos

#### 3.1 Comparativa Factory vs Prototype

* **Contenido** (\~300 palabras): cuándo elegir cada patrón para IaC, costes de serialización profundas vs creación directa y mantenimiento.

#### 3.2 Patrones avanzados: Adapter (código de referencia)

* **Implementación**:

  ```python
  # adapter.py
  class MockBucketAdapter:
      def __init__(self, null_block: dict):
          self.null = null_block

      def to_bucket(self) -> dict:
          # Mapear triggers a parámetros de bucket simulado
          name = list(self.null["resource"]["null_resource"].keys())[0]
          return {
              "resource": {
                  "mock_cloud_bucket": {
                      name: {"name": name, **self.null["resource"]["null_resource"][name]["triggers"]}
                  }
              }
          }
  ```
* **Prueba**: Inserta en builder y exporta un recurso `mock_cloud_bucket`.

#### 3.3 Tests automatizados con pytest

* **Ejemplos**:

  ```python
  def test_singleton_meta():
      a = ConfigSingleton("X"); b = ConfigSingleton("Y")
      assert a is b

  def test_prototype_clone_independent():
      proto = ResourcePrototype(NullResourceFactory.create("app"))
      c1 = proto.clone(lambda b: b.__setitem__("foo", 1))
      c2 = proto.clone(lambda b: b.__setitem__("bar", 2))
      assert "foo" not in c2 and "bar" not in c1
  ```

#### 3.4 Escalabilidad de JSON

* **Tarea**: Mide tamaño de `terraform/main.tf.json` para `build_null_fleet(15)` vs `(150)`.
* **Discusión**: impacto en CI/CD, posibles estrategias de fragmentación.

#### 3.5 Integración con Terraform Cloud (opcional)

* **Esquema**: `builder.export_to_cloud(workspace)` usando API HTTP.
* **Diagrama**: Flujo desde `generate_infra.py` -> `terraform login` -> `apply`.

> **Entrega final**:
>
> * Informe comparativo y código de Adapter.
> * Suite de tests.
> * Análisis de escalabilidad.
> * (Opcional) Documento con flujo de integración a Terraform Cloud.
