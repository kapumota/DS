### 1. Contextualización y propósito de mocks y stubs en entornos DevOps

En las organizaciones que adoptan prácticas DevOps, la colaboración entre equipos de desarrollo, operaciones y calidad es esencial para acelerar el ciclo de entrega de software y reducir el riesgo de fallos en producción. 
En este ecosistema, la automatización de pruebas desempeña un papel fundamental: permite detectar errores de forma temprana, garantizar el cumplimiento  de requisitos y dar confianza a los equipos para realizar despliegues frecuentes. 
No obstante, la ejecución de una suite de pruebas completa puede volverse prohibitiva si cada test depende de servicios externos, bases de datos reales o 
infraestructuras complejas.
Ante este reto surge la necesidad de los dobles de prueba, en particular, mocks y stubs como mecanismos para aislar unidades de código, simular 
comportamientos controlados y validar la lógica interna sin vínculos a recursos externos.

El uso de stubs y mocks encaja de forma natural dentro de un pipeline de CI/CD: simplifica la configuración del entorno, acelera el feedback loop tras
cada commit y disminuye la fragilidad de las pruebas al eliminar puntos de fallo ajenos al propio código.
Al abstraer las dependencias externas, los equipos pueden diseñar pruebas unitarias robustas que ejecuten en milisegundos, lo que permite integrar 
validaciones en cada fase del pipeline, desde la etapa "pre-commit" hasta las pruebas de integración y despliegue sin sacrificar velocidad ni fiabilidad.

En este contexto, profundizar en las diferencias conceptuales, variantes y patrones de uso de mocks y stubs resulta esencial para diseñar suites de pruebas coherentes, mantenibles y alineadas con los objetivos de DevOps: entregar valor de forma continua, con alta calidad y riesgo controlado.


### 2. Definiciones fundamentales y matices conceptuales

#### 2.1 Stub: respuestas predefinidas y control de datos

Un **stub** es un doble de prueba cuyo único propósito es servir datos deterministas al código bajo prueba. Cuando una función o método realiza una llamada a un servicio externo, por ejemplo una API REST o una consulta a una base de datos, el stub intercepta esa llamada y retorna un valor fijo preconfigurado. 
De este modo, se garantiza que el test siempre reciba la misma información, independientemente del estado real del sistema o de la red.

**Características clave de los stubs:**

* **Respuestas fijas**: los valores de retorno están codificados en el stub o se cargan desde fixtures (archivos JSON, YAML, etc.).
* **Simplicidad**: carecen de lógica interna más allá de devolver el resultado esperado.
* **Velocidad**: como no requieren comunicación de red ni acceso a disco, sus respuestas son casi inmediatas.
* **Predecibilidad**: eliminan la variabilidad asociada a datos en tiempo real, facilitando pruebas deterministas.

**Ejemplo de uso**: suponer que un módulo realiza una petición a un endpoint externo para obtener la configuración de feature flags. Un stub suministra siempre el mismo JSON de configuración, lo que permite validar la lógica de activación de flags sin depender del servicio real.

#### 2.2 Mock: verificación de interacciones y metadatos

Un **mock** va un paso más allá de un stub: no solo suministra respuestas, sino que también registra información sobre cómo se ha llamado. Esto incluye el tipo de método invocado, los argumentos pasados y el número de veces que se ha ejecutado la llamada.
Los mocks facilitan la comprobación de contratos de interacción entre componentes y permiten asegurar que un servicio colateral se invoca de forma correcta en distintos escenarios.

**Características clave de los mocks:**

* **Registro de llamadas**: guardan metadatos en estructuras internas, accesibles al finalizar el test.
* **Aserciones de comportamiento**: se pueden verificar expectativas como `mock.assert_called_with(...)` o `mock.assert_not_called()`.
* **Side effects**: mediante el uso de parámetros como `side_effect`, el mock puede simular excepciones, retardos o devoluciones dinámicas.
* **Medición de acoplamiento**: al registrar cada interacción, el mock evidencia qué tan estrechamente vinculado está el código a sus dependencias.

**Ejemplo de uso**: en un escenario donde un servicio de procesamiento de pagos debe notificar a otro sistema tras confirmar una transacción, un mock permite comprobar que el método `notificar_transaccion` se invoca exactamente una vez con los parámetros correctos, sin necesitar un endpoint real.

| Aspecto        | Stub                                    | Mock                                                |
| -------------- | --------------------------------------- | --------------------------------------------------- |
| Rol principal  | Proveer datos deterministas             | Simular dependencias y registrar interacciones      |
| Tipo de lógica | Ausente o mínima                        | Puede incorporar `side_effect` y lógica condicional |
| Velocidad      | Muy alta (sin overhead de verificación) | Alta (ligeramente más lento por registro interno)   |
| Aserciones     | Basadas en el resultado                 | Basadas en el número y contenido de las llamadas    |



### 3. Otras variantes de dobles de prueba y su aplicación en DevOps

Además de mocks y stubs, la clasificación general de dobles de prueba incluye diversas categorías pensadas para casos concretos. Conocerlas ayuda a elegir la herramienta más adecuada según el nivel de aislamiento y complejidad que requiera cada test:

#### 3.1 Fake

Un **fake** es una implementación simplificada pero funcional de la dependencia real. Por ejemplo, una base de datos en memoria construida sobre SQLite o un repositorio que guarda datos en una estructura de datos local (listas, diccionarios). 
Los fakes conservan parte de la lógica de producción, lo que permite realizar tests más cercanos a la realidad sin necesidad de desplegar servicios completos.

* **Uso típico**: pruebas de integración ligeras, validación de reglas de negocio cuando se desea conservar la semántica de consulta y persistencia.
* **Ventajas**: más rápido de configurar que la infraestructuras reales, mantiene consistencia funcional.
* **Limitaciones**: puede no reproducir comportamientos de concurrencia o escalabilidad de la versión productiva.

#### 3.2 Spy

Un **spy** se construye a partir de una instancia real, a la que se envuelve con un mecanismo de registro. 
El spy delega las llamadas al objeto real y, además, "espía" qué métodos se invocan y con qué argumentos. Es útil cuando se quiere comprobar el efecto de cierta operativa en el objeto original sin prescindir por completo de su comportamiento.

* **Uso típico**: validar que un componente modifica el estado de otro objeto de forma adecuada, manteniendo la lógica original.
* **Ventajas**: comportamiento de producción con metadatos de llamada.
* **Limitaciones**: riesgo de acoplamiento alto, ya que depende de la implementación real.

#### 3.3 Dummy

Un **dummy** es un objeto sin funcionalidad que se pasa únicamente para completar la lista de parámetros de un método. No se usa realmente dentro de la prueba y no registra llamadas. Suele emplearse para cumplir firmas y evitar la creación de objetos innecesarios.

* **Uso típico**: tests donde solo interesa una parte de las dependencias, y las demás se rellenan de forma genérica.
* **Ventajas**: simplicidad máxima.
* **Limitaciones**: no aporta valor más allá de la firma.

### 4. Patrones de uso de mocks y stubs en pipelines de CI/CD

#### 4.1 Integración temprana en el pipeline

La filosofía Shift-Left, inherente a DevOps, propone desplazar las pruebas hacia etapas iniciales del ciclo de desarrollo. En este enfoque, los mocks y stubs deben insertarse en:

1. **Pre-commit hooks**: ejecutar tests unitarios ligeros con stubs para garantizar que cada commit basa su calidad en pruebas que corren en milisegundos.
2. **Build stage**: en la etapa de compilación y empaquetado, incorporar un conjunto más amplio de tests con mocks, que verifiquen contratos de interacción.
3. **Gate de integración**: antes de permitir el merge en la rama principal, ejecutar todos los tests unitarios y de integración simulados mediante fakes y mocks, evitando dependencias externas.

De este modo, se consigue un feedback loop veloz que detecta errores de lógica y de integración de interfaz antes de que ocupen recursos de infraestructura más costosos.

#### 4.2 Separación de entornos y parametrización

En pipelines complejos, es habitual contar con múltiples entornos de pruebas:

* **Unit tests**: aislados con stubs y mocks, configurados en variables de entorno tipo `TEST_MODE=unit`.
* **Integration tests**: usando fakes o containers efímeros (por ejemplo, instancias Docker de base de datos), definidos con `TEST_MODE=integration`.
* **End-to-end tests**: conectando a entornos de staging reales o mediante infraestructuras provisionales.

La parametrización de fixtures y la inyección de dependencias basada en la variable de entorno permiten reutilizar el mismo código de prueba en distintas fases del pipeline, tan solo cambiando la configuración de mocks, fakes o servicios reales.

#### 4.3 Simulación de fallos y resiliencia

Uno de los grandes beneficios de mocks y stubs es la posibilidad de emular errores de red, excepciones de servicios o latencias elevadas:

* **Timeouts**: configurar un stub para que arroje una excepción de tipo `TimeoutError`, permitiendo validar la lógica de reintento (`retry`) y los circuit breakers.
* **Códigos de error HTTP**: simular respuestas 4xx o 5xx para comprobar la correcta gestión de errores en clientes REST.
* **Datos corruptos**: retornar payloads incompletos o malformados para asegurar que el parser maneja de forma robusta los escenarios de datos inválidos.

Estas simulaciones aumentan la cobertura de casos límite sin necesidad de manipular el entorno real, mejorando la calidad y la resiliencia del sistema final.

En el ámbito de DevOps, el diseño de una estrategia de pruebas efectiva requiere atender tanto a la velocidad de retroalimentación como a la confiabilidad de la validación. En este sentido, la literatura especializada distingue dos líneas de pensamiento con filosofías complementarias: la escuela Classical (London School) y la escuela Mockist (Detroit School). 

#### 4.4. Classical testing (London School)

La escuela Classical pone el énfasis en la integridad del sistema al ejecutar pruebas que incorporan múltiples componentes en sus versiones reales. En lugar de sustituir dependencias críticas por simulaciones, este enfoque prefiere levantar entornos lo más parecidos posible a producción, ejecutando la lógica de negocio, el acceso a bases de datos y las comunicaciones entre servicios.

* **Integración real de componentes.** Cada prueba involucra varias capas de la aplicación: controladores HTTP, lógica de negocio, acceso a datos y, en su caso, colas de mensajes o servicios externos.
* **Configuración de entornos.** Se utilizan contenedores Docker o entornos de staging que replican la infraestructura productiva. La preparación de datos puede requerir scripts de inicialización de bases de datos y la orquestación de varios contenedores de servicios dependientes.
* **Cobertura de extremo a extremo.** Estas pruebas buscan validar flujos completos, por ejemplo, desde la recepción de una solicitud REST hasta la persistencia y la publicación de eventos, garantizando que todas las piezas encajan y cooperan correctamente.

*Ventajas principales:*

1. **Alta confianza en la cohesión del sistema.** Un fallo en una prueba rara vez es espurio: indica con precisión una incompatibilidad real entre módulos, interpretación errónea de datos o problemas de configuración.
2. **Detección de fallos de integración.** Se descubren errores de serialización, de mapeo de entidades y de configuración de servicios que pasarían desapercibidos en pruebas puramente unitarias.

*Desventajas clave:*

1. **Mayor tiempo de ejecución.** Al tener que desplegar contenedores, inicializar bases de datos y ejecutar lógica completa, cada suite puede tardar desde decenas de segundos hasta varios minutos.
2. **Complejidad de mantenimiento.** La gestión de entornos complejos, scripts de inicialización y redes de contenedores incrementa la carga operativa, y un cambio en la infraestructura puede romper varias pruebas simultáneamente.

*Ejemplo práctico:*
En un pipeline de GitLab CI, se define un stage "integration-tests" que levanta un stack con Docker Compose, ejecuta migraciones en una base de datos PostgreSQL y luego lanza pruebas con pytest. Cada job destruye el entorno al finalizar, pero el tiempo medio de ejecución de la suite puede rondar los 3–5 minutos.

**4.5. Mockist Testing (Detroit School)**
Por contraste, la escuela Mockist prioriza la velocidad y el aislamiento estricto de cada unidad de código. Casi todas las dependencias externas se reemplazan por objetos simulados (mocks), lo que permite tests muy rápidos y centrados en verificar contratos de interacción y lógica interna.

* **Aislamiento máximo.** Cada prueba se enfoca en una única clase o función; todas las colaboraciones externas (repositorios, clientes HTTP, servicios de mensajería) se simulan con mocks.
* **Verificación de contratos.** Se comprueba no solo el resultado de una operación, sino que los mocks hayan sido invocados con los parámetros correctos y en el orden previsto.
* **Ejecutables en milisegundos.** Al no requerir arranque de contenedores ni acceso a recursos externos, las pruebas unitarias mockeadas pueden completarse en cuestión de milisegundos, facilitando su inclusión en pre-commit hooks y verificación continua.

*Ventajas principales:*

1. **Retroalimentación instantánea.** El desarrollador obtiene información inmediata tras cada modificación, fomentando un desarrollo ágil y iterativo.
2. **Detección temprana de rupturas de interfaz.** Cambios en la firma de métodos o en los parámetros de llamadas se detectan de forma inmediata, evitando propagaciones de errores a etapas posteriores.

*Desventajas clave:*

1. **Fragilidad de pruebas.** Al fijar el comportamiento de mocks en detalles internos, incluso modificaciones inofensivas en la implementación pueden romper pruebas, generando falsas alarmas y frustración.
2. **Falsos negativos en integración.** Escenarios que funcionan con datos simulados pueden fallar cuando se prueban en un entorno real, por ejemplo, diferencias de serialización de fechas o límites de tamaño de payload.

*Ejemplo práctico:*
Con pytest y unittest.mock, un test de servicio de notificaciones podría definirse así:

```python
def test_enviar_alerta(mock_sender):
    mock_sender.send.return_value = True
    resultado = servicio_alertas.procesar_y_enviar(mock_sender, datos)
    mock_sender.send.assert_called_once_with(datos)
    assert resultado is True
```

En este caso, la prueba comprueba tanto la invocación del método `send` como el resultado, sin necesidad de un servicio real de mensajería.


**4.5. Estrategia combinada y equilibrio en DevOps**
La verdadera fortaleza de una estrategia de pruebas DevOps radica en la combinación de ambos enfoques:

1. **Shift-Left con Mockist:** en etapas tempranas (pre-commit, build rápido), ejecutar exclusivamente tests unitarios con mocks y stubs, garantizando un feedback loop inmediato.
2. **Pruebas de integración classical:** en gates previos a la rama principal y en entornos de staging, ejecutar una batería de tests que involucren contenedores efímeros y fakes realistas, validando flujos de extremo a extremo.
3. **Monitoreo y métricas:** aplicar métricas DORA al pipeline de pruebas, midiendo tiempo de ejecución, frecuencia de fallos y tiempo de recuperación de suite. Esto permite ajustar porcentajes de cobertura y decidir el balance óptimo entre velocidad y profundidad de pruebas.

Al articular un plan que aproveche la agilidad de los mocks y la exhaustividad de las pruebas de integración, los equipos DevOps consiguen un pipeline robusto y rápido, capaz de detectar tanto errores de interfaz como problemas de cohesión del sistema, sin sacrificar velocidad ni fiabilidad.


#### 5. Implementación práctica con pytest y herramientas de mocking

#### 5.1 Configuración de fixtures en pytest

pytest destaca por su potente sistema de fixtures, que facilita la creación de stubs y mocks de manera declarativa:

```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def servicio_stub():
    stub = Mock()
    stub.obtener_datos.return_value = {"usuario": "alice", "id": 42}
    return stub

def test_procesar_datos(servicio_stub):
    from mi_app import procesar_datos
    resultado = procesar_datos(servicio_stub)
    assert resultado == "Usuario alice con ID 42"
    servicio_stub.obtener_datos.assert_called_once()
```

En este ejemplo, la fixture `servicio_stub` proporciona al test un stub configurado que devuelve datos predefinidos. La verificación de la llamada se realiza mediante `assert_called_once()`, que actúa como mock.

#### 5.2 Uso de parametrización y side effects

Para probar múltiples escenarios sin duplicar código, pytest permite parametrizar inputs y simular efectos secundarios:

```python
@pytest.mark.parametrize("respuesta,esperado", [
    ({"usuario": "bob", "id": 7}, "Usuario bob con ID 7"),
    ({"usuario": "", "id": None}, "Datos incompletos"),
])
def test_procesar_varios(servicio_stub, respuesta, esperado):
    servicio_stub.obtener_datos.return_value = respuesta
    from mi_app import procesar_datos
    assert procesar_datos(servicio_stub) == esperado
```

Para simular excepciones:

```python
def test_procesar_fallo(servicio_stub):
    servicio_stub.obtener_datos.side_effect = TimeoutError("Tiempo excedido")
    from mi_app import procesar_datos
    with pytest.raises(TimeoutError):
        procesar_datos(servicio_stub)
```

#### 5.3 Integración con herramientas de cobertura y métricas

En un pipeline DevOps, es fundamental medir la calidad y el rendimiento de las pruebas:

* **Coverage.py** integrado con pytest para generar informes de cobertura de líneas, ramas y funciones. Se puede configurar un umbral mínimo (por ejemplo, 85 %) que bloquee el merge si no se alcanza.

  ```bash
  pytest --cov=mi_app --cov-fail-under=85
  ```

* **pytest-benchmark** para detectar regresiones de tiempo. Permite comparar métricas de duración entre ejecuciones y generar alertas si sobrepasan un umbral.

  ```python
  def test_benchmark_procesar(benchmark, servicio_stub):
      from mi_app import procesar_datos
      benchmark(lambda: procesar_datos(servicio_stub))
  ```

El resultado se integra en el pipeline, almacenando metadatos en sistemas de monitoreo y generando gráficos históricos de tendencias.


### 6. Lógica dinámica en mocks: uso de `side_effect`

En entornos DevOps, donde los pipelines de integración continua deben ofrecer feedback rápido y fiable, resulta imprescindible simular comportamientos de dependencias externas de forma realista. La propiedad `side_effect` de los mocks en frameworks como `unittest.mock` o pytest permite enriquecer estas simulaciones con lógica dinámica, abarcando escenarios que van mucho más allá del simple retorno estático.

#### 6.1 Errores transitorios y reintentos automáticos

En sistemas distribuidos, los errores transitorios, como timeouts o interrupciones temporales de red— son inevitables. Para validar que los componentes reaccionan de forma correcta (por ejemplo, implementando estrategias de retry con backoff exponencial o circuit breakers), podemos simular una secuencia de excepciones y valores exitosos:

```python
from unittest.mock import Mock
import pytest

@pytest.fixture
def servicio_stub():
    mock = Mock()
    # Primer llamado lanza TimeoutError, segundo devuelve datos válidos
    mock.obtener_datos.side_effect = [TimeoutError("timeout"), {"id": 1, "valor": "x"}]
    return mock

def test_retry(servicio_stub):
    from mi_app import cliente_api
    resultado = cliente_api.obtener_con_retry(servicio_stub, max_intentos=2)
    assert resultado == {"id": 1, "valor": "x"}
    assert servicio_stub.obtener_datos.call_count == 2
```

En este ejemplo, `cliente_api.obtener_con_retry` debe capturar la primera excepción, esperar un retraso y volver a llamar antes de finalmente obtener un dato válido. Las pruebas validan tanto la lógica de reintento como el comportamiento ante éxito parcial. Esta aproximación aporta confianza en que el pipeline de CI/CD detectará regressions en las políticas de reintento sin necesidad de interconectar sistemas reales.

#### 6.2 Respuestas secuenciales y paginación

Muchas APIs externas, como servicios de almacenamiento o colas de mensajes, devuelven datos paginados. Con `side_effect` podemos emular distintas respuestas en sucesivas invocaciones:

```python
def paginas(*args, **kwargs):
    # simula tres llamadas: página 1, página 2 y fin de datos
    for pagina in [{"items": [1,2]}, {"items": [3,4]}, {"items": []}]:
        yield pagina

mock_api.side_effect = paginas()

def test_paginacion(mock_api):
    from mi_app import recolector
    todos = recolector.recoger_todos(mock_api)
    assert todos == [1,2,3,4]
    assert mock_api.call_count == 3
```

Aquí, `side_effect` recibe un generador que va produciendo distintos payloads, permitiendo al test asegurar que el algoritmo de paginación consume todos los elementos correctamente.

#### 6.3 Validaciones on-the-fly

Cuando es necesario garantizar que los parámetros enviados a una dependencia cumplan ciertos criterios, podemos definir una función de validación:

```python
def validar_parametros(*args, **kwargs):
    assert isinstance(kwargs.get('usuario_id'), int), "usuario_id debe ser entero"
    if kwargs.get('retry') not in (True, False):
        raise ValueError("retry inválido")
    return {"status": "OK"}

mock_repo.side_effect = validar_parametros

def test_parametros(mock_repo):
    from mi_app import servicio
    resultado = servicio.procesar(usuario_id=123, retry=True)
    assert resultado["status"] == "OK"
```

Con esta técnica, la mock no solo verifica la invocación sino que ejecuta lógica interna que comprueba tipos, rangos y formatos, lanzando errores si algo se desví­a de lo esperado. Esto evita la escritura de múltiples tests centrados en validación de parámetros y refuerza la robustez de las pruebas.

#### 6.4 Técnicas de patching: localizado y holístico

El patching es la técnica de sustitución de funciones, clases o módulos enteros para redirigir llamadas a implementaciones simuladas. En pytest y `unittest.mock` existen varias formas de aplicar parches, que van desde ámbitos muy concretos hasta toda la sesión de pruebas.

#### 6.4 Patching localizado

**Context manager**
Se utiliza para encapsular un bloque de código en el cual una función o método queda parcheado:

```python
from unittest.mock import patch

def test_funcion_loc():
    with patch('modulo.extern.funcion_externa') as mock_func:
        mock_func.return_value = 42
        from mi_app import operacion
        assert operacion() == 42
```

**Decorador de test**
Aplica el parche únicamente al alcance de la función de test:

```python
from unittest.mock import patch

@patch('modulo.servicio_externo')
def test_aislado(mock_serv):
    mock_serv.get_data.return_value = []
    from mi_app import handler
    assert handler() == []
```

**Ventajas del enfoque localizado**

* El parche solo afecta el bloque o función concreta, reduciendo el riesgo de interferencias con otros tests.
* Facilita la comprensión del contexto: al leer el test queda claro qué se está simulando.
* Mantiene la configuración de fixtures y mocks limpia y específica.

#### 6.5 Patching holístico

En pruebas de integración parcial o en escenarios donde múltiples tests requieren el mismo parche, se pueden emplear fixtures con alcance amplio:

```python
import pytest

@pytest.fixture(scope='session', autouse=True)
def parche_db(monkeypatch):
    from mi_app.fake_db import FakeDB
    fake_db = FakeDB()
    monkeypatch.setattr('app.database.connect', lambda: fake_db)
    return fake_db
```

**Ventajas del enfoque holístico**

* Se define una única vez para toda la sesión o módulo, evitando duplicar setup.
* Ideal para entornos donde las pruebas requieren un backend simulado estable, como una base de datos en memoria.
* Reduce el tiempo de inicialización si el fake o stub es costoso de crear.

**Consideraciones**

* Un patch de alcance amplio puede esconder efectos secundarios entre tests, por lo que es crucial asegurar que el fake o stub maneje la limpieza de estado entre ejecuciones.
* Para tests unitarios sucios, es preferible el patching localizado, reservando el enfoque holístico para pruebas de integración ligera.


#### 6.6. Parametrización y principio Open/Closed

La parametrización de tests es fundamental para cubrir múltiples escenarios con un único bloque de código, respetando el **Principio Open/Closed** (abierto a extensión, cerrado a modificación). pytest facilita dicha técnica mediante el marcador `@pytest.mark.parametrize`, lo que redunda en:

* **Mayor mantenibilidad**: añadir nuevos casos sin tocar la lógica del test.
* **Cobertura variada**: sintetizar casos nominales, bordes y de error en un único decorador.
* **Claridad**: la lista de casos queda visible en la cabecera del test, facilitando revisiones.

```python
import pytest

@pytest.mark.parametrize("entrada,esperado", [
    ("", 0),
    ("a", 1),
    ("abc", 3),
    ("hola mundo", 10),
])
def test_longitud(entrada, esperado):
    from mi_app.utils import calcular_longitud
    assert calcular_longitud(entrada) == esperado
```

Este patrón se extiende a tests con mocks:

```python
@pytest.mark.parametrize("side_effect,resultado_esperado", [
    ([TimeoutError], pytest.raises(TimeoutError)),
    ([{"value": 1}], lambda: True),
])
def test_reintento_variado(monkeypatch, side_effect, resultado_esperado):
    import mi_app.cliente as cliente
    def fake_obtener():
        yield from side_effect
    mock = Mock()
    mock.obtener.side_effect = fake_obtener()
    if isinstance(resultado_esperado, type(pytest.raises)) and resultado_esperado == pytest.raises(TimeoutError):
        with pytest.raises(TimeoutError):
            cliente.obtener_con_retry(mock)
    else:
        assert cliente.obtener_con_retry(mock) is True
```

Aquí la parametrización abarca tanto la simulación de errores como el comportamiento exitoso, respetando OCP al no alterar el cuerpo del test.

#### 6.7 Autospec: garantizar adherencia a la interfaz real

Con el envejecimiento de la base de código, las firmas de funciones o métodos pueden cambiar, induciendo desincronizaciones silenciosas en los mocks clásicos. La técnica **autospec** crea mocks que respetan exactamente la firma de la implementación real, detectando llamadas con parámetros inválidos en tiempo de prueba:

```python
from unittest.mock import create_autospec

def test_autospec():
    from mi_app.servicios import ServicioReal
    mock_serv = create_autospec(ServicioReal, instance=True)
    # esto lanza TypeError si llamamos con parámetros inválidos
    mock_serv.procesar_dato("valor_correcto")
```

**Beneficios de autospec en DevOps**

* **Detección temprana de incompatibilidades**: evita que tests mockeados acepten llamadas desfasadas de la API real.
* **Refuerzo de DIP**: al depender de la interfaz, no de la implementación, facilita invertir dependencias y promueve inyección de mocks coherente.
* **Documentación viva**: el propio mock refleja la definición actual de la clase o función, sirviendo como verificación de la API.

Se recomienda aplicar autospec en bibliotecas internas críticas y en aquellas piezas de código con alta rotación de parámetros.

#### 6.8 Inspección de historial de llamadas y verificaciones avanzadas

Los mocks no solo registran si fueron llamados, sino que almacenan un historiales detallado de todas las invocaciones, sus argumentos y orden. Esta capacidad es esencial en arquitecturas de eventos y pipelines de datos, donde el orden y la frecuencia de llamadas puede afectar la integridad del sistema.

#### 6.9 Uso de `call_args_list`

```python
from unittest.mock import Mock, call

mock = Mock()
# supongamos que el sistema llama a mock.a(1) y luego a mock.b(2, x=3)
mock.a(1)
mock.b(2, x=3)

assert mock.call_args_list == [call.a(1), call.b(2, x=3)]
```

#### 6.9 Verificaciones específicas

* **`assert_called_once_with(...)`**: garantiza que la llamada se hizo exactamente una vez con los argumentos dados.
* **`assert_any_call(...)`**: comprueba que al menos una de las llamadas coincide con los parámetros.
* **Orden de invocaciones**: comparar listas ordenadas de llamadas para validar flujos críticos.

```python
mock_serv.assert_called_once_with(usuario_id=123, retry=True)
mock_serv.assert_any_call('param1')
```

Estas técnicas permiten asegurar que, por ejemplo, un pipeline de procesamiento de mensajes invoque primero la etapa de deserialización, luego la validación y finalmente la persistencia, en el orden correcto.


#### 6.10 Gestión de marcas `skip` y `xfail` en flujos CI/CD

En desarrollos ágiles y en continuo movimiento, es habitual que ciertos tests dependan de condiciones temporales o entornos específicos. pytest ofrece marcadores para gestionar estos casos sin comprometer la estabilidad del pipeline completo.

#### 6.11 `@pytest.mark.skip`

Se utiliza cuando un test no aplica en determinadas circunstancias. Por ejemplo, si una funcionalidad solo existe en versiones recientes de Python o requiere un servicio externo no disponible:

```python
import sys
import pytest

@pytest.mark.skipif(sys.platform != "linux", reason="Solo soportado en Linux")
def test_solo_linux():
    # ...
```

Los tests marcados como `skip` no se ejecutan, pero quedan registrados en el informe.

#### 6.12 `@pytest.mark.xfail`

Se emplea para tests que actualmente fallan por un bug conocido o dependencia en desarrollo. El fallo se considera "esperado" y no detiene la suite, aunque se informa para seguimiento:

```python
@pytest.mark.xfail(reason="Bug #123: manejo de fecha incorrecto", strict=True)
def test_fecha_limite():
    from mi_app import calcular_fecha_limite
    assert calcular_fecha_limite("2025-02-29") == "2025-03-01"
```

* **`strict=True`**: si el test pasa inesperadamente, se considera un error, forzando la revisión de la marca.
* **Informe JUnit XML**: los pipelines de CI en GitHub Actions, Azure Pipelines o Jenkins pueden procesar estos informes para diferenciar tests exitosos, fallidos, xfailed y skip.

#### 6.13 Estrategias de mantenimiento

* **Revisión periódica**: acumular muchos `xfail` o `skip` sin resolver incrementa la deuda técnica. Se recomienda agendar tareas trimestrales para limpiar marcas obsoletas.
* **Integración con alertas**: configurar que, si el ratio de tests marcados supera un umbral (por ejemplo, 5 % del total), se dispare una alerta en Slack o correo.
* **Contextualización en los reports**: incluir en la documentación del proyecto las razones y fechas de creación de cada marca, facilitando su seguimiento.

Con una gestión adecuada de `skip` y `xfail`, los equipos mantienen la fluidez del despliegue continuo, evitando bloqueos por fallos esperados mientras preservan visibilidad sobre la salud de la suite de pruebas.


### 7. Buenas prácticas y recomendaciones para mocks y stubs en DevOps

1. **Limitar la complejidad de los mocks**: evite simular toda la lógica de un servicio. Para casos complejos, prefiera un fake o un container efímero.
2. **Mantener los tests deterministas**: no dependa de datos generados aleatoriamente ni de relojes del sistema,  utilice fixtures y parametrización controlada.
3. **Documentar los contratos de mock/stub**: registre en la documentación o en comentarios de código qué comportamientos se están simulando y con qué propósito.
4. **Revisar periódicamente la alineación con el servicio real**: cada vez que cambie la API de una dependencia, actualice los mocks para reflejar nuevos endpoints o formatos de datos.
5. **Evitar mocks excesivos**: si un test necesita más de tres niveles de mocks, quizás esté probando demasiado, y sea mejor escribir un test de integración con un entorno real o un fake.
6. **Integrar en la cultura de equipo**: educar a los desarrolladores y a los ingenieros de QA sobre cuándo usar mocks, stubs, fakes o containers, promoviendo un estilo de prueba coherente.
7. **Automatizar la limpieza de entornos**: asegúrese de que los stubs y mocks no dejen artefactos temporales ni persistan datos que puedan interferir con otros tests.
8. **Medir la efectividad**: utilice métricas de cobertura fría (líneas, ramas) y caliente (pruebas en producción) para ajustar la estrategia de mocks y stubs con base en datos reales.
