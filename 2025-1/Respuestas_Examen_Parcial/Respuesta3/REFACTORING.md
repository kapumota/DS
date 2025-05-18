### Informe de refactorización – Ejemplo RuleProcessor

#### 1. Violaciones SOLID identificadas en `validator_module_legacy.py`

El módulo `validator_module_legacy.py` presentaba varias violaciones a los principios SOLID:

| Principio SOLID                      | Violación específica en `validator_module_legacy.py`                                                                                                                                                                                               |
|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **SRP (Principio de responsabilidad única)** | La clase `RuleProcessor` era responsable de múltiples tareas: leer reglas desde archivo o codificadas, obtener configuración de una fuente externa simulada, evaluar condiciones de reglas (usando `eval()` directamente), registrar errores y además orquestar todo el proceso de validación. Demasiadas responsabilidades para una sola clase. |
| **OCP (Principio abierto/cerrado)** | La clase estaba cerrada a la extensión pero no abierta. Cualquier cambio en la forma de obtener reglas (ej. desde una base de datos), la fuente de configuración o la lógica de evaluación de condiciones requería modificar internamente la clase `RuleProcessor`. |
| **LSP (Principio de sustitución de Liskov)** | Aunque no se rompía flagrantemente al no haber jerarquía de herencia directa, si se intentara crear una subclase de `RuleProcessor` para alterar, por ejemplo, solo la evaluación de condiciones, sería complicado sin romper la lógica o el contrato esperado por la clase base, debido al fuerte acoplamiento de sus métodos privados. |
| **ISP (Principio de segregación de interfaces)** | Los consumidores de `RuleProcessor` no podían depender solo de la funcionalidad de "procesamiento de reglas". Forzosamente dependían de toda la maquinaria interna de carga de reglas, configuración, logging y evaluación, incluso si solo querían una parte. No existían interfaces específicas para roles más pequeños. |
| **DIP (Principio de inversión de dependencias)** | La clase `RuleProcessor` dependía directamente de implementaciones concretas: `logging.getLogger` para el logging, `Path("rules.conf").open()` para la carga de reglas, la función `_get_external_config` para la configuración, y la función `eval()` para la evaluación de condiciones. No dependía de abstracciones. |

#### 2. Correcciones aplicadas en `validator_module_refactored.py`

Las violaciones SOLID fueron abordadas en `validator_module_refactored.py` de la siguiente manera:

* **SRP (Responsabilidad única):**
    * `RuleProcessor` ahora se enfoca *únicamente* en orquestar el proceso de validación: obtiene las reglas y la configuración de fuentes externas, itera sobre los datos y, para cada elemento, itera sobre las reglas delegando la evaluación de cada condición a un colaborador especializado.
    * Las responsabilidades de obtener reglas, obtener configuración, registrar logs y evaluar condiciones se extrajeron a componentes separados (colaboradores inyectados).

* **DIP (Inversión de dependencias):**
    * Se introdujeron **Protocolos** (`RuleSource`, `ConfigSource`, `ConditionEvaluator`, `Logger`) que actúan como abstracciones para las dependencias.
    * `RuleProcessor` ahora depende de estas abstracciones, no de implementaciones concretas. Esto permite que las implementaciones concretas de estas dependencias puedan ser intercambiadas fácilmente (ej. para pruebas o para cambiar la fuente de datos).
    * Las políticas de alto nivel (en `RuleProcessor`) ya no dependen de los detalles de bajo nivel (cómo se cargan las reglas o se evalúan las condiciones).

* **OCP (Abierto/Cerrado):**
    * Gracias a la dependencia de abstracciones (protocolos), se pueden introducir nuevas fuentes de reglas (ej. `DatabaseRuleSource`), nuevas formas de obtener configuración o nuevas estrategias de evaluación de condiciones (`AdvancedConditionEvaluator`) sin modificar el código de `RuleProcessor`. La clase está abierta a la extensión a través de nuevas implementaciones de sus dependencias.

* **ISP (Segregación de interfaces):**
    * Los protocolos definidos son interfaces cohesivas y específicas para cada rol (`RuleSource` solo para obtener reglas, `Logger` solo para loguear, etc.). Los clientes (en este caso, `RuleProcessor`) dependen solo de las interfaces que necesitan. Si otros componentes necesitaran solo una parte de la funcionalidad (ej. solo el evaluador), podrían depender directamente de esa abstracción.

#### 3. Variantes de inyección de dependencias (DI) demostradas

Se demostraron las siguientes variantes de Inyección de Dependencias:

1.  **Inyección por constructor:** Es la forma principal de DI utilizada en `RuleProcessor`. Las dependencias cruciales (`rule_source`, `config_source`, `evaluator`) se proveen como argumentos al constructor `__init__`. El `logger` también se puede inyectar por constructor, con un `_NullLogger` como fallback si no se provee.
2.  **Inyección por Setter (o método):** `RuleProcessor` expone métodos como `set_condition_evaluator(evaluator: ConditionEvaluator)` y `set_logger(logger: Logger)`. Esto permite cambiar una dependencia específica (la estrategia de evaluación o el logger) después de que el objeto ha sido instanciado. Es útil para cambiar comportamientos dinámicamente o para facilitar ciertas configuraciones en pruebas.

#### 4. Patrones de diseño aplicados

Se aplicaron los siguientes patrones de diseño:

* **Strategy (Estrategia):** El `ConditionEvaluator` es un ejemplo claro. Define una familia de algoritmos (formas de evaluar una condición), encapsula cada uno y los hace intercambiables. `SafeConditionEvaluator` es una estrategia concreta, y en las pruebas se usó `AlwaysTrueEvaluator` como otra estrategia. `RuleProcessor` trabaja con la interfaz `ConditionEvaluator` sin conocer la implementación específica.
* **Null Object (Objeto Nulo):** La clase `_NullLogger` implementa la interfaz `Logger` pero sus métodos no hacen nada. Se utiliza como un logger por defecto cuando no se inyecta uno explícitamente en `RuleProcessor`, evitando la necesidad de comprobaciones `if logger is not None:` en múltiples lugares del código.
* **Protocol (Abstracción / Interfaz):** Aunque no es un patrón GoF clásico, el uso de `typing.Protocol` en Python es clave para definir las abstracciones de las dependencias, permitiendo un "duck typing" estructural y formalizando los contratos que las dependencias deben cumplir.

#### 5. Mejoras en la testeabilidad

La refactorización y la aplicación de DI mejoraron drásticamente la testeabilidad:

* **Aislamiento de unidades:** `RuleProcessor` puede ser probado en aislamiento de sus dependencias reales (ficheros, servicios externos, lógica compleja de evaluación) utilizando dobles de prueba (fakes, stubs, mocks).
* **Fakes y Stubs:** En `tests/conftest.py`, se crearon implementaciones "fake" como `MemoryRuleSource`, `MemoryConfigSource` y `ListCapturingLogger` que simulan el comportamiento de las dependencias reales de una manera controlada para las pruebas.
* **Fixtures de Pytest:** Se utilizan extensivamente para configurar el entorno de prueba, instanciar datos de entrada y proveer las dependencias (fakes o mocks) al `RuleProcessor` bajo prueba. Esto reduce el código boilerplate en los tests.
* **Mocks (con `pytest-mock`):** Se demostró el uso de `mocker.MagicMock` (o `mocker.spy`) para verificar interacciones específicas con las dependencias, como asegurar que el método `error` de un logger fue llamado con los argumentos correctos.
* **Pruebas de estrategias individuales:** La lógica de evaluación de condiciones (`SafeConditionEvaluator`) ahora puede ser probada de forma independiente y exhaustiva.
* **Escenarios de prueba claros:** Es fácil simular diferentes conjuntos de reglas, configuraciones, datos de entrada y comportamientos de las dependencias para cubrir diversos escenarios.
* **Marcadores `@pytest.mark.xfail` y `@pytest.mark.skip`:** Se utilizaron para documentar y gestionar pruebas que dependen de condiciones externas o recursos no siempre disponibles, mejorando la robustez y el significado de la suite de pruebas.

#### 6. Automatización del proyecto

Se implementó la siguiente automatización:

* **`Makefile`:** Proporciona un punto de entrada único y simple (`make test`) para ejecutar la suite de pruebas completa, incluyendo la generación de reportes de coverage. También incluye targets adicionales como `clean`, `lint` (opcional) y `setup` (opcional) para facilitar tareas comunes de desarrollo.
* **Git hook (`pre-push`):** Se configuró un hook de pre-push que se ejecuta automáticamente antes de cada `git push`. Este hook:
    -  Ejecuta `make test` para asegurar que todas las pruebas pasan.
    -  Valida que los mensajes de los commits que se están empujando sigan el formato de commits convencionales.
    Si alguna de estas comprobaciones falla, el push es abortado, ayudando a mantener la calidad y la consistencia en el repositorio.

#### 7. Manejo de la complejidad algorítmica y de datos

El diseño refactorizado, gracias a la abstracción de responsabilidades y la inyección de dependencias, está bien preparado para manejar incrementos en la complejidad algorítmica o de las estructuras de datos:

* **Estructuras de reglas complejas:** Si las reglas tuvieran dependencias entre sí (por ejemplo, un motor de reglas que procesa un grafo de reglas) o fueran anidadas, una implementación más sofisticada de `RuleSource` podría encapsular esta lógica sin impactar al `RuleProcessor`.
* **Preprocesamiento de datos:** Si los datos de entrada requirieran ordenamiento, filtrado, enriquecimiento o transformaciones antes de la validación, estas operaciones podrían encapsularse dentro de una implementación especializada de `RuleSource` o como un paso previo.
* **Lógica de evaluación avanzada:** El patrón Strategy para `ConditionEvaluator` permite sustituir `SafeConditionEvaluator` por implementaciones que parseen lenguajes de condiciones más complejos (DSLs) o que interactúen con sistemas externos.
* **Escalabilidad y rendimiento:** Al separar la obtención de reglas, configuración y la evaluación, se pueden optimizar estas partes de forma independiente (ej. caching en `RuleSource`, optimizaciones en `ConditionEvaluator`).

La separación de  preocupaciones asegura que `RuleProcessor` se mantenga enfocado en la orquestación, mientras que la complejidad intrínseca se delega a componentes especializados, facilitando el desarrollo y las pruebas aisladas.
