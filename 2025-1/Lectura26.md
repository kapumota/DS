### Patrones de diseño aplicados a módulos de infraestructura en Terraform

En el ámbito de la Infraestructura como Código (IaC), la correcta organización de los componentes, ya sean archivos HCL, JSON o clases generadoras en Python, resulta determinante para asegurar escalabilidad, mantenibilidad y coherencia. Cuando diseñamos proyectos de Terraform, especialmente si empleamos recursos `null_resource` con 
provisioners locales para simular la provisión de recursos sin depender de proveedores cloud, la adopción de patrones de diseño clásicos del desarrollo de software  aporta grandes beneficios. 

#### 1. Contextualización y objetivos

La IaC transforma la gestión de infraestructura en un problema de desarrollo: describir estados deseados, versionarlos, probarlos y desplegarlos de forma automática. Sin embargo, conforme crecen la cantidad de entornos, se multiplican los recursos y se diversifican las configuraciones, el código tenderá al desorden si no aplicamos metodologías sólidas de diseño. La implementación de ejemplo utiliza:

- **Terraform JSON** con proveedor `null`, simulando el aprovisionamiento local mediante `local-exec`.
- **Clases Python** que generan los bloques JSON de recursos: fábricas, prototipos y builders.
- **Un orquestador (`main.py`)** que ensambla todos los módulos en un único `main.tf.json`.

El objetivo es ilustrar cómo cada patrón de diseño facilita tareas concretas:

1. Evitar instancias duplicadas (Singleton).
2. Representar jerarquías compuestas (Composite).
3. Desacoplar la lógica de creación (Factory).
4. Reutilizar configuraciones base (Prototype).
5. Construir objetos complejos por pasos (Builder).

#### 2. Patrón Singleton: instancia única garantizada

##### Principio y utilidad

El patrón **Singleton** asegura que una clase tenga una única instancia durante el ciclo de vida de la aplicación y provee un punto de acceso global. En IaC, es útil para recursos que deben existir una sola vez, como:

- Un **bucket centralizado de logs**.
- Una **VPC compartida** entre varios entornos o microservicios.
- **Políticas de seguridad** globales.

#### Implementación avanzada

Nuestra clase `VpcSingleton` trabaja así:

1. **Chequeo estático**: la variable `_instance` es `None` hasta la primera creación.
2. **Sobrescritura de `__new__`**: si `_instance` es `None`, creamos la instancia y almacenamos propiedades (por ejemplo, el CIDR de la VPC).
3. **Acceso global**: cualquier llamada posterior a `VpcSingleton()` retorna la misma instancia configurada.

El método `build()` genera un bloque Terraform JSON con `null_resource` y un provisioner que escribe en un archivo `vpc.txt`:

```python
class VpcSingleton:
    _instance = None

    def __new__(cls, cidr="10.0.0.0/16"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.cidr = cidr
        return cls._instance

    def build(self):
        return {
            "vpc": {
                "triggers": {"always_run": "${timestamp()}"},
                "provisioner": {"local-exec": {"command": f"echo 'VPC CIDR={self.cidr}' > vpc.txt"}}
            }
        }
```

#### Beneficios y limitaciones

- **Beneficios**:
  - Evita que se declare accidentalmente más de una VPC.
  - Simplifica el acceso a la configuración desde cualquier módulo.

- **Limitaciones**:
  - Oculta estado en variables estáticas, lo que complica tests aislados.
  - Puede convertirse en un cuello de botella si la instancia gestiona lógica compleja.

#### 3. Patrón Composite: jerarquías recursivas

#### Principio fundamental

El patrón **Composite** trata de manera homogénea objetos indivisibles ("hojas") y conjuntos de objetos ("compuestos"). Se basa en:

1. **Componente común**: una interfaz o clase abstracta que define la operación (`build_all`).
2. **Nodo hoja**: implementa la interfaz y realiza la acción concreta (por ejemplo, una fábrica individual).
3. **Nodo compuesto**: contiene una colección de componentes, reenvía la llamada recursivamente a sus hijos.

####  Implementación en IaC

Creamos `CompositeModule` que almacena referencias a instancias de distintos módulos (Singleton, Factory, Prototype, Builder). Al invocar `build_all()`, recorre todos los hijos y combina sus bloques JSON:

```python
class CompositeModule:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, module):
        self.children.append(module)

    def build_all(self):
        combined = {}
        for child in self.children:
            block = child.build()
            combined.update(block)
        return combined
```

En la orquestación final hacemos:

```python
root = CompositeModule("infra_root")
root.add(vpc_singleton)
root.add(DatabaseFactory())
root.add(NetworkFactory())
root.add(RawModule(subnet1))
root.add(RawModule(subnet2))
root.add(RawModule(app_server))

tf_config = {
    "resource": {"null_resource": root.build_all()}
}
```

#### Ventajas y desafíos

- **Ventajas**:
  - Refleja explícitamente la organización jerárquica de la infraestructura.
  - Aísla módulos: el root no necesita conocer los detalles internos de cada componente.

- **Desafíos**:
  - Puede generar árboles muy profundos, lo que dificulta diagnósticos de errores.
  - La composición excesiva puede impactar el rendimiento al construir el JSON final.

#### 4. Patrón Factory: delegar creación

#### Concepto y propósito

El patrón **Factory** define una interfaz para crear objeto, en nuestro caso, bloques Terraform JSON y delega la responsabilidad concreta a subclases:

- `DatabaseFactory` genera el recurso de base de datos.
- `NetworkFactory` crea la red.
- `ServerFactory` construye instancias de servidor.

#### Implementación detallada

Cada fábrica hereda de `BaseFactory` e implementa `build()` retornando un diccionario con un único recurso `null_resource`:

```python
class BaseFactory:
    def build(self) -> dict:
        raise NotImplementedError

class DatabaseFactory(BaseFactory):
    def build(self):
        user = os.getenv("USER", "local")
        return {
          "database": {
            "triggers": {"always_run": "${timestamp()}"},
            "provisioner": {"local-exec": {"command": f"echo 'DB={user}' > database.txt"}}
          }
        }
```

El orquestador itera sobre una colección de fábricas:

```python
for factory in factories:
    tf_config["resource"]["null_resource"].update(factory.build())
```

#### Ventajas y consideraciones

- **Ventajas**:
  - **Desacoplamiento**: las fábricas encapsulan la lógica de creación, mientras el orquestador solo las consume.
  - **Extensibilidad**: agregar un nuevo tipo de recurso solo requiere añadir una nueva subclase.

- **Consideraciones**:
  - En infraestructuras muy sencillas, la sobrecarga de clases puede resultar innecesaria.
  - Las fábricas deben exponer interfaces coherentes para facilitar su uso en el Composite.

#### 5. Patrón Prototype: clonación de plantillas

#### Fundamento teórico

El **Prototype** permite crear nuevos objetos copiando ("clonando") una instancia prototipo y modificando solo los atributos necesarios. Esto resulta muy útil cuando:

- Los bloques JSON comparten una configuración base compleja.
- Queremos generar múltiples subredes, instancias u otros recursos con ligeras variaciones.

#### Implementación avanzada

La clase `ResourcePrototype` guarda una plantilla y ofrece `clone(overrides)`:

```python
class ResourcePrototype:
    def __init__(self, template):
        self.template = template

    def clone(self, **overrides):
        cfg = json.loads(json.dumps(self.template))  # copia profunda
        key = next(iter(cfg))
        cfg[key]["provisioner"]["local-exec"]["command"] = overrides.get(
            "command", cfg[key]["provisioner"]["local-exec"]["command"]
        )
        return cfg
```

Ejemplo de uso:

```python
subnet_proto = ResourcePrototype({
  "subnet": {
    "triggers": {"always_run": "${timestamp()}"},
    "provisioner": {"local-exec": {"command": "echo 'Base Subnet' > subnet.txt"}}
  }
})

sn1 = subnet_proto.clone(command="echo 'Subnet 10.0.1.0/24' > subnet-1.txt")
sn2 = subnet_proto.clone(command="echo 'Subnet 10.0.2.0/24' > subnet-2.txt")
```

#### Beneficios y precauciones

- **Beneficios**:
  - Minimiza la duplicación de código y reduce el riesgo de inconsistencias.
  - Facilita la generación dinámica de recursos análogos.

- **Precauciones**:
  - Cambios posteriores en la plantilla original no se reflejarán en clones ya creados.
  - Requiere un manejo cuidadoso de la copia profunda si la configuración es muy anidada.


#### 6. Patrón Builder: construcción paso a paso

####  Filosofía del patrón

El **Builder** abstrae la creación de un objeto complejo mediante una secuencia de pasos encadenados (fluent interface). En IaC, un recurso puede requerir múltiples atributos opcionales (tags, zonas, tamaños, usuarios), por lo que un builder:

1. Expone métodos específicos (por ejemplo, `set_name()`, `set_zone()`, `add_tag()`).
2. Valida internamente cada parámetro.
3. Genera la representación final solo al invocar `build()`.

#### Implementación detallada

Nuestro `ServerBuilder` implementa:

```python
class ServerBuilder:
    def __init__(self):
        self.config = {}

    def set_name(self, name):
        self.config["name"] = name
        return self

    def set_zone(self, zone):
        self.config["zone"] = zone
        return self

    def add_tag(self, key, value):
        self.config.setdefault("tags", {})[key] = value
        return self

    def build(self):
        name = self.config.get("name", "server")
        cmd = f"echo 'Server {name} en zona {self.config.get('zone')}' > {name}.txt"
        return {
          name: {
            "triggers": {"always_run": "${timestamp()}"},
            "provisioner": {"local-exec": {"command": cmd}}
          }
        }
```

####  Ventajas y desafíos

- **Ventajas**:
  - Claridad: cada parámetro se define de forma explícita.
  - Seguridad: el builder puede validar valores antes de la generación.

- **Desafíos**:
  - Verbosidad: aumenta la cantidad de código en infraestructuras simples.
  - Curva de aprendizaje: requiere entender la interfaz fluent.

#### 7. Criterios para seleccionar el patrón adecuado

A la hora de decidir qué patrón aplicar, recomendamos valorar estos aspectos:

1. **Grado de reutilización**:
   - Si necesitas declarar un recurso global una única vez, aplica **Singleton**.
   - Si vas a clonar múltiples configuraciones basadas en plantillas, usa **Prototype**.

2. **Complejidad de configuración**:
   - Pocas propiedades y construcciones directas: **Factory**.
   - Muchas opciones y validaciones: **Builder**.

3. **Estructura jerárquica**:
   - Varias capas de dependencias (VPC -> subredes -> instancias): **Composite**.

4. **Escalabilidad y mantenimiento**:
   - Proyectos pequeños o pilotos: **Factory** y **Prototype** bastan.
   - Sistemas empresariales con múltiples módulos: combina **Composite** y **Builder**.

5. **Pruebas y validación**:
   - Facilita tests unitarios evitando Singletons ocultos. Builder y Factory son más testables.

6. **Evolución del proyecto**:
   - Si la infraestructura va a crecer y diversificarse, invierte en Composite + Builder.
   - Para scripts rápidos o prototipos, Factory y Prototype ofrecen simplicidad.

**Notas importantes**

* **Mejora de la reutilización y consistencia**
  Al aplicar Factory, Prototype y Builder, evitamos duplicar bloques JSON y garantizamos que las configuraciones compartidas evolucionen de forma coherente. Esto reduce el riesgo de incongruencias entre entornos y simplifica la adopción de cambios masivos.

* **Control y centralización de recursos críticos**
  El patrón Singleton permite gestionar de forma explícita recursos que deben existir una única vez (VPC, buckets de logs, políticas globales), evitando provisiones accidentales múltiples y asegurando un punto de acceso uniforme.

* **Modelado explícito de jerarquías**
  Composite refleja de manera natural la relación padre-hijo entre módulos (por ejemplo, VPC -> subredes -> servidores), facilitando tanto la lectura del código como la orquestación recursiva de todos los componentes de la infraestructura.

* **Desacoplamiento y extensibilidad**
  Al delegar la generación de recursos en objetos Factory o Builder, se separa la "lógica de negocio" de la "lógica de construcción", de modo que añadir un nuevo tipo de recurso o un nuevo parámetro no implica tocar el orquestador principal, sino solamente crear o extender la clase correspondiente.

* **Facilidad de pruebas y validación**
  Patrón Builder y Factory, al exponer interfaces claras y evitar estados ocultos, permiten escribir tests unitarios sobre la generación de bloques Terraform (por ejemplo, validando JSON resultante), mientras que los Singleton deben usarse con cautela pues complican el aislamiento.

* **Escalabilidad y mantenibilidad**
  Para proyectos pequeños o prototipos rápidos, basta con Factory y Prototype. A medida que la infraestructura crece en complejidad, la combinación de Composite con Builder ofrece una estructura modular que escala de forma predecible y mantiene el código organizado.

* **Decisión informada según contexto**
  Seleccionar el patrón adecuado depende de factores como el número de instancias deseadas, la complejidad de configuración, la jerarquía de dependencias y la necesidad de validación previa. Una arquitectura mixta, aprovechando lo mejor de cada patrón, suele ser la solución más robusta en entornos empresariales.
