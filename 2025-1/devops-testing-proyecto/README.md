### Ejemplo sobre testing y  DevOps  con SOLID

Este ejemplo demuestra la aplicación de los principios SOLID en suites de pruebas automatizadas dentro de pipelines DevOps sin depender de workflows de GitHub Actions.
Incluye:

* Implementación de lógica de negocio sencilla (gestión de usuarios y pagos).
* Inversión e inyección de dependencias mediante fixtures de **pytest**.
* Ejemplos de mocks y stubs aplicando SRP, OCP, LSP, ISP y DIP.

#### Ejecución de pruebas

```bash
pytest -v
```

#### Estructura

```
src/devops_testing/        # Código de producción
tests/                     # Pruebas unitarias
tests/integration/         # Pruebas de integración
```

####  Principios SOLID aplicados al testing
La filosofía SOLID, originaria del desarrollo orientado a objetos, se extiende al diseño de suites de pruebas:

**Single Responsibility Principle (SRP)**

Una prueba debe validar un único comportamiento o requisito.

Beneficio: Claridad en la causa de un fallo y facilidad de mantenimiento.

**Open/Closed Principle (OCP)**

La suite debe poder ampliarse para nuevos casos sin modificar tests existentes.

Ejemplo conceptual: parametrizar escenarios en lugar de duplicar lógica.

**Liskov Substitution Principle (LSP)**

Los fakes o mocks utilizados deben cumplir la misma interfaz que las implementaciones reales.

Resultado: Al sustituir componentes reales por simulados, el comportamiento general permanece consistente.

**Interface Segregation Principle (ISP)**

Evitar pruebas que dependan de interfaces demasiado amplias.

Aplicación: Dividir fixtures o helpers en funcionalidades concretas (por ejemplo, datos de usuario vs. conexión a servicios).

**Dependency Inversion Principle (DIP)**

Las pruebas dependen de abstracciones (interfaces), no de implementaciones concretas.

Implicación: Facilita la inyección de stubs, mocks o fakes sin acoplarse a detalles internos.

#### Inversión de dependencias e inyección de dependencias (DI)
En pytest, la inyección de dependencias se realiza principalmente a través de fixtures. 

Conceptualmente:

**DI mediante fixtures**

Los tests declaran sus dependencias (bases de datos, clientes HTTP, configuraciones) en la firma de la función, y pytest las inyecta.

Ventaja: Aísla el setup/teardown y centraliza la configuración, alineándose con DIP y SRP.

**Variantes de DI**

- Constructor-like (fixture que actúa como fábrica de objetos configurados).

- Setter-like (fixture que provee una función de configuración o parcheo).

- Interface-driven (fixture que implementa la interfaz mínima esperada por la lógica de negocio).

Mediante DI se consigue desacoplar tests de implementaciones concretas, permitiendo substituciones fáciles en entornos de CI/CD o despliegue.
