### Automatización de testing en DevOps 

En un entorno de desarrollo marcado por metodologías ágiles y arquitecturas de microservicios, la calidad del software es hoy una necesidad crítica y no un atributo opcional. En este contexto, las prácticas de DevOps han evolucionado hacia procesos altamente automatizados y colaborativos, donde la integración continua (CI) y el despliegue continuo (CD) permiten validar la calidad del código de forma sistemática a lo largo del ciclo de vida del desarrollo.

Cada nueva línea de código activada en el repositorio inicia de inmediato una serie de validaciones que examinan la funcionalidad y solidez de la aplicación. Esto sustituye los antiguos ciclos de prueba manual por mecanismos automáticos que abarcan desde tests unitarios hasta pruebas de aceptación, simulando flujos de usuario reales. Lo más importante es que esta validación es continua, proporcionando retroalimentación rápida para prevenir regresiones y fomentar una cultura de calidad compartida dentro del equipo.

La eficiencia de un pipeline de pruebas bien diseñado reside en su equilibrio entre exhaustividad y velocidad. Las pruebas unitarias se encargan de asegurar el comportamiento de funciones y módulos de manera aislada. Las pruebas de integración validan el correcto funcionamiento de la aplicación en conjunto, incluyendo bases de datos efímeras y servicios auxiliares desplegados temporalmente en contenedores. Por su parte, las pruebas de aceptación o end-to-end, mediante herramientas como Playwright o Selenium, replican la experiencia del usuario y documentan su ejecución con capturas de pantalla o grabaciones.

El diseño de estos pipelines puede seguir una estructura declarativa, donde los pasos incluyen instalación de dependencias, ejecución de test con herramientas como `pytest`, generación de informes de cobertura, configuración de entornos temporales (por ejemplo, un contenedor de PostgreSQL), y pruebas completas que validan escenarios de usuario. Cada paso debe estar claramente delimitado y responder a condiciones lógicas de ejecución: no se deben iniciar pruebas de integración si las unitarias fallan, ni ejecutar pruebas de interfaz si hay fallos estructurales.

Otro aspecto esencial en la eficiencia del pipeline es la gestión del tiempo. Técnicas como el almacenamiento temporal de dependencias (caching de `pip` o `node_modules`) o la ejecución paralela de pruebas con distintas versiones de lenguaje o sistema operativo, permiten acelerar significativamente el proceso sin comprometer la cobertura.

Para controlar la ejecución simultánea en entornos compartidos, se establecen estrategias de concurrencia: evitar que dos ejecuciones corran sobre la misma rama al mismo tiempo o cancelar automáticamente pipelines obsoletos si se reciben múltiples commits en rápida sucesión. Asimismo, el uso de dependencias explícitas entre tareas asegura un flujo lógico, donde los pasos de integración dependen del éxito de las pruebas unitarias.

La gestión de artefactos —como reportes de cobertura, logs o binarios generados— es otro componente clave. Estos artefactos se intercambian entre tareas del pipeline y se almacenan para su análisis posterior. Esto permite la trazabilidad completa de una ejecución y facilita el diagnóstico de errores, incluso días después del evento.

La seguridad también forma parte integral de la automatización del testing. Las credenciales y tokens deben ser gestionados mediante mecanismos seguros, nunca codificados directamente en los scripts. Además, el acceso a entornos de prueba debe estar restringido por el principio de mínimos privilegios, y los análisis automáticos de dependencias pueden evitar la introducción de bibliotecas con vulnerabilidades conocidas.

A medida que los equipos escalan, también lo hacen sus necesidades de mantener coherencia entre múltiples repositorios o módulos. Para esto, se utilizan plantillas reutilizables que definen estructuras comunes de pruebas, así como filtros por ruta que aseguran que solo se ejecuten pruebas pertinentes al código que ha sido modificado. Esto reduce la carga innecesaria en los pipelines y mejora los tiempos de respuesta.

La documentación de los pipelines —ya sea en forma de archivos `README` específicos o convenciones de marcado dentro de los tests— ayuda a su mantenimiento a largo plazo. Estas convenciones incluyen categorización de pruebas con etiquetas (`@unit`, `@integration`, etc.) o separación de escenarios críticos y optativos.

Finalmente, la evolución de los pipelines contempla también pruebas no directamente relacionadas con el código fuente. Esto incluye validaciones sobre infraestructura como código (IaC), revisión de licencias de software y pruebas de rendimiento automatizadas que simulan cargas reales para medir métricas como latencia y throughput.

Un pipeline robusto de testing en DevOps, incluso sin depender de plataformas específicas, puede estructurarse con base en los siguientes principios fundamentales:

1. **Automatización integral**: ejecución automática de pruebas unitarias, de integración y de extremo a extremo en cada commit.
2. **Optimización del tiempo**: uso de caching, paralelización y matrices de entornos para mejorar la eficiencia.
3. **Calidad y seguridad**: incorporación de reglas de protección de ramas, escaneos de vulnerabilidades y gestión segura de secretos.
4. **Trazabilidad completa**: manejo de artefactos, análisis de cobertura y reportes de ejecución como elementos de auditoría.
5. **Reutilización y escalabilidad**: adopción de estructuras comunes y mecanismos de ejecución selectiva según el contexto del cambio.

Al estructurar pipelines sobre estas bases, los equipos pueden integrar calidad en cada fase del ciclo de vida del software, favoreciendo el despliegue rápido, la detección temprana de errores y la evolución ordenada de sistemas complejos.



### SOLID y  testing

En los entornos de desarrollo actuales, donde los ciclos de entrega se miden en minutos y las arquitecturas se despliegan en contenedores efímeros, el *testing* automatizado debe integrarse de manera orgánica con la filosofía **DevOps**. 
Lejos de ser meros conjuntos de comandos que se ejecutan tras cada *commit*, las suites de pruebas se convierten en un componente vivo que evoluciona junto al código de producción. Para que esa evolución sea sostenible, resulta esencial aplicar los principios de diseño **SOLID**, no únicamente al código que se despliega, sino también al propio diseño de las pruebas.

Al adoptar la visión de que cada caso de prueba es, en sí mismo, un pequeño fragmento de software con sus propias responsabilidades, dependencias y efectos secundarios, podemos elevar la calidad de la suite al mismo nivel de rigor que exigimos al *core* de negocio. A continuación exploramos cómo cada principio SOLID encuentra su correspondencia natural en el *testing*, acompañándolo de ejemplos de código autocontenidos y comentados para evidenciar los desafíos que resuelven y los beneficios que aportan.


### 1  Single Responsibility Principle (SRP)

Un **test** debe responder a una sola pregunta. Cuando esa idea se viola, la función de prueba acaba conteniendo ramas, bucles y múltiples *asserts* que difuminan el motivo real de un fallo.

```python
# tests/test_precios.py
import pytest

from tienda.precio import calcular_precio_final

@pytest.mark.unit
def test_descuento_cliente_frecuente():
    """
    SRP: sólo valida la regla de descuento para cliente frecuente.
    Cualquier fallo implica que la política de descuentos cambió
    o dejó de respetarse.
    """
    subtotal = 100.0          # precio de lista
    es_cliente_frecuente = True
    esperado = 90.0           # 10 % de descuento
    
    resultado = calcular_precio_final(subtotal, es_cliente_frecuente)
    assert resultado == pytest.approx(esperado)
```

*Puntos clave*

* El *fixture* implícito es mínimo: un precio y un flag.
* No se crea un carrito, ni se simula stock; **SRP** se mantiene intacto.


#### 2  Open/Closed Principle (OCP)

Queremos añadir casos sin tocar la lógica de prueba. La parametrización de **pytest** nos abre la puerta:

```python
# tests/test_redondeo.py
import pytest
from tienda.redondeo import redondear

CASOS = [
    # cantidad,  esperado
    (2.499, 2.50),
    (2.444, 2.44),
    (5.995, 6.00),  # nuevo caso agregado sin modificar el test
]

@pytest.mark.parametrize("cantidad,esperado", CASOS)
def test_redondeo_05_centimos(cantidad, esperado):
    """
    OCP: el test no cambia cuando agregamos tuplas a CASOS.
    """
    assert redondear(cantidad) == pytest.approx(esperado)
```

Con esta estructura, ampliar la cobertura se reduce a añadir datos y no a reescribir oraciones de prueba, cumpliendo **OCP**.

#### 3  Liskov Substitution Principle (LSP)

Los *doubles* de prueba deben respetar la interfaz real. Con `autospec=True` forzamos esa equivalencia:

```python
# app/repositorio.py
class RepositorioDB:
    def obtener(self, id_: int) -> dict: ...
    def guardar(self, registro: dict) -> int: ...

# tests/test_servicio.py
import pytest
from unittest.mock import create_autospec
from app.servicio import ServicioNegocio
from app.repositorio import RepositorioDB

@pytest.fixture
def repo_mock():
    # LSP: el mock hereda la firma exacta de RepositorioDB
    return create_autospec(RepositorioDB, instance=True)

def test_obtener_invoca_repo(repo_mock):
    svc = ServicioNegocio(repo=repo_mock)

    repo_mock.obtener.return_value = {"id": 1, "valor": 42}
    resultado = svc.obtener_transformado(1)

    repo_mock.obtener.assert_called_once_with(1)
    assert resultado == 84  # lógica de negocio duplica el valor
```

Si la firma real cambia (p. ej. `id` --> `identificador`), el mock detectará de inmediato el error, garantizando que **LSP** se respeta.

#### 4  Interface Segregation Principle (ISP)

En lugar de una mega-*fixture*, se crean piezas pequeñas y composables:

```python
# tests/conftest.py
import pytest
from tienda.models import Usuario
from tienda.db import SessionLocal

@pytest.fixture
def conexion_bd():
    """Solo abre una sesión de BD; nada más."""
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def usuario_autenticado(conexion_bd):
    """Crea un usuario y lo devuelve logueado."""
    user = Usuario(nombre="Ana")
    conexion_bd.add(user)
    conexion_bd.commit()
    return user

@pytest.fixture
def cliente_http(app):    # fixture que monta FastAPI TestClient
    from fastapi.testclient import TestClient
    return TestClient(app)
```

Un test que sólo necesita leer datos puede combinar `conexion_bd` y `cliente_http`, mientras que otro, centrado en permisos, añade `usuario_autenticado`. Cada fixture mantiene una **interfaz estrecha y específica**, cumpliendo **ISP**.

#### 5  Dependency Inversion Principle (DIP)

El código de producción depende de abstracciones, y los tests inyectan implementaciones concretas o *fakes*.

```python
# dominio/puertos.py
from abc import ABC, abstractmethod
from typing import Protocol

class IRepositorioMensajes(Protocol):
    @abstractmethod
    def guardar(self, mensaje: str) -> None: ...
    @abstractmethod
    def obtener_todos(self) -> list[str]: ...

# infraestructura/repos_sqlite.py
import sqlite3
from dominio.puertos import IRepositorioMensajes

class RepoSQLite(IRepositorioMensajes):
    ...

# servicio.py
from dominio.puertos import IRepositorioMensajes

class ServicioMensajeria:
    def __init__(self, repo: IRepositorioMensajes):
        self._repo = repo

    def publicar(self, msg: str) -> None:
        self._repo.guardar(msg.upper())

# tests/test_servicio_mensajeria.py
from dominio.puertos import IRepositorioMensajes
from servicio import ServicioMensajeria

class RepoEnMemoria(IRepositorioMensajes):
    def __init__(self):
        self._datos: list[str] = []
    def guardar(self, mensaje: str) -> None:
        self._datos.append(mensaje)
    def obtener_todos(self):
        return self._datos

def test_publicar_mayusculas():
    repo = RepoEnMemoria()
    svc  = ServicioMensajeria(repo)

    svc.publicar("hola devops")
    assert repo.obtener_todos() == ["HOLA DEVOPS"]
```

**DIP** queda patente: el servicio desconoce si la persistencia termina en SQLite, DynamoDB o un *fake* en memoria; sólo sabe que hay una abstracción que cumple `IRepositorioMensajes`.

#### 6  Métricas y disciplina DevOps (cobertura, *flakiness*, *benchmark*)

Una suite bien SOLID facilita la instrumentación de métricas. Con **pytest-cov** y **pytest-benchmark** se imponen umbrales automáticos:

```ini
# pyproject.toml (fragmento)
[tool.pytest.ini_options]
addopts = """
    -ra
    --cov=tienda
    --cov-report=term-missing
    --benchmark-min-rounds=5
"""
markers = [
    "unit: pruebas unitarias ultra rápidas",
    "integration: pruebas de integración reales",
]

[tool.coverage.report]
fail_under = 80      # bloquea el pipeline si bajamos de 80 %
```

```python
# tests/benchmark/test_algoritmo.py
import numpy as np

def algoritmo_costoso(n: int) -> float:
    return np.sum(np.sqrt(np.arange(n)))

def test_algoritmo_benchmark(benchmark):
    # benchmark repetirá la función y registrará latencias
    resultado = benchmark(algoritmo_costoso, 10_000)
    # aserción simple para evitar falsos positivos de benchmark-only
    assert resultado > 0
```

Al integrarse en el *pipeline*, cualquier degradación de rendimiento o caída de cobertura genera un *gate* automático, manteniendo la calidad sin intervención humana constante.

####  Refactor progresivo de suites heredadas

Cuando se hereda una base de 2000 pruebas acopladas y lentas, se aplica la estrategia **Boy-Scout**:

1. Cada vez que se toca un módulo de código, se identifica su test correspondiente.
2. Se divide en funciones independientes (SRP).
3. Se parametriza (OCP).
4. Se sustituyen dobles por *autospec* (LSP).
5. Se extraen fixtures granulares (ISP).
6. Se inyectan las dependencias a través de protocolos o *interfaces* (DIP).

Una parte de la suite queda modernizada en cada *sprint*, sin frenar el desarrollo funcional.

### Inversión de dependencias (DIP)

La Inversión de dependencias (DIP) traslada la responsabilidad de conocer las implementaciones concretas desde las capas de alto nivel, reglas de negocio, orquestadores de dominio, servicios de aplicación— hacia un punto de ensamblaje externo. En ecosistemas DevOps, donde las aplicaciones se reconstruyen en contenedores o entornos efímeros varias veces al día, esta separación posibilita reemplazar componentes críticos (motores de base de datos, servicios de mensajería, gateways externos) sin alterar las reglas de negocio ni los tests que las vigilan.

#### Fixtures como mecanismo de inyección de dependencias en pytest

Pytest ejerce la inyección de dependencias (DI) mediante la resolución automática de fixtures. Cada nombre que aparece en la firma de una función de prueba es tratado como un requisito que se satisfará en tiempo de ejecución:

* **Declaración explícita de necesidades**
  El test enumera *qué* necesita —no *cómo* obtenerlo—. Pytest se encarga de crear o localizar la fixture y entregarla. Este gesto materializa DIP, porque el test conversa con una abstracción (la fixture) y desconoce los detalles de conexión, credenciales, rutas internas o flujos de autenticación.

* **Separación de setup y teardown**
  La lógica de preparación y liberación vive dentro de la fixture, no en el test. Al quedar centralizada, puede versionarse, revisarse y endurecerse (por ejemplo, enmascarar secretos) igual que cualquier otro artefacto de la infraestructura.

* **Alineación con SRP**
  Cada fixture encarna una sola responsabilidad: abrir un túnel a un clúster de Kubernetes, generar un token JWT, o sembrar datos mínimos en una tabla temporal. Al componer varias fixtures se consigue un entorno completo, pero cada pieza sigue siendo indivisible desde el punto de vista del cambio.


#### Tres variantes habituales de DI con fixtures

| Variante             | Idea central                                                                       | Situación típica en pipelines DevOps                                                                                                                                   |
| -------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Constructor-like** | La fixture actúa como fábrica: crea y devuelve un objeto ya configurado.           | Construir instancias ligadas a *feature flags* del entorno de despliegue (por ejemplo, un *feature store* apuntando a sandbox o producción).                           |
| **Setter-like**      | La fixture proporciona una función que aplica parches, *monkey-patches* o *hooks*. | Redirigir llamadas a terceros hacia un *stub* local cuando se ejecuta en un runner con red restringida.                                                                |
| **Interface-driven** | La fixture implementa solo los métodos exigidos por la capa de dominio.            | Facilitar que el mismo test funcione contra SQLite en memoria, Postgres dentro de Docker o un servicio gestionado en la nube, girando únicamente variables de entorno. |


#### Integración en flujos DevOps

1. **Elasticidad de entornos efímeros**

   * En la fase *unit* de un *merge request*, todas las fixtures apuntan a servicios embebidos (SQLite, Redis Fake, S3 localstack).
   * Al llegar al *job* de integración, variables de entorno provocan que las mismas fixtures inyecten URL de contenedores de Docker Compose levantados ad-hoc.
   * En *staging*, la configuración se resuelve vía *secret manager* y la inyección conecta con servicios gestionados —sin cambiar una sola línea de los tests—.

2. **Observabilidad y trazabilidad**
   Las fixtures pueden adjuntar *labels* o *spans* a las transacciones que generan. Al inyectar un cliente HTTP instrumentado, cada petición contiene cabeceras de *trace-id*. Ello permite que el stack de observabilidad correlacione los tests con métricas de latencia, detecte cuellos de botella y alerte degradaciones antes de prod.

3. **Gobernanza de datos**
   Mediante DI, la suite elige entre un dataset anonimizado (*snapshot* nightly) o un generador sintético de registros GDPR-safe. Los runners ejecutan la misma batería de pruebas con datos reales sanitizados en *pre-prod* y con datos ficticios en *CI*, garantizando cobertura regulatoria sin exponer PII.

4. **Estrategias *chaos-friendly***
   Una fixture parametrizada puede envolver a la dependencia con un *proxy* que introduce fallos probabilísticos (latencias, *timeouts*, respuestas corruptas). Activando un *flag* en el pipeline de *nightly chaos*, los tests validan la resiliencia de la lógica ante perturbaciones, cumpliendo el principio de fallos anticipados.

5. **Versionado progresivo**
   Cuando una librería de dominio evoluciona (v1 -> v2), se añade una fixture "adaptadora” que implementa ambas interfaces y decide en tiempo de ejecución a cuál versión delegar. Los tests se ejecutan dos veces, una por versión, proporcionando visibilidad temprana de incompatibilidades.


#### Puntos de alineación con principios SOLID

* **DIP**-- Los tests formulan sus expectativas respecto a contratos semánticos (fixtures), no respecto a tipos concretos ni detalles de infraestructura.
* **SRP** -- Cada fixture concentra una única responsabilidad operativa; el test se mantendrá pequeño y legible.
* **OCP** -- Al requerir un nuevo backend o una nueva variante de inyección, se añade una ruta condicional a la fixture existente (o una fixture adicional) sin tocar los tests ya aprobados.
* **LSP** -- Las variantes *fake* o *spy* cumplen la misma interfaz mínima que el recurso de producción, garantizando intercambiabilidad.
* **ISP** --Las fixtures evitan exponer funcionalidad sobrante; sólo publican lo que la capa de negocio invoca, minimizando acoplamiento.


La práctica de DI con fixtures no solo facilita la escritura de pruebas robustas; se convierte en una estrategia de diseño operativo que habilita pipelines reproducibles, enriquece la observabilidad y acelera la detección de regresiones, todo ello mientras sostiene la promesa de despliegues continuos confiables.

#### Variantes de DI

#### Constructor-like fixtures

**Descripción:**
Estos fixtures funcionan como fábricas preconfiguradas que devuelven instancias "listas para usar" de componentes pesados o complejos: clientes HTTP, conexiones a bases de datos, clientes de colas de mensajería o incluso objetos que envuelven autenticación y autorización completas.

**Características clave:**

* **Inicialización única:** la construcción del objeto (que puede implicar handshake, autenticación o carga de configuración) se realiza una única vez por sesión de test (scope `session` o `module`), reduciendo la sobrecarga en comparación con inicializaciones repetidas.
* **Reuse a nivel de suite:** al definirse con scope amplio, el fixture garantiza que todos los tests que lo requieran reciban la misma instancia o una instancia equivalente, evitando inicializaciones redundantes.
* **Configuración centralizada:** parámetros como URLs, credenciales o timeouts se parametrizan en un mismo lugar, facilitando modificaciones globales.

**Ejemplo (pytest):**

```python
import pytest
import requests

@pytest.fixture(scope="session")
def http_client():
    # Imagina un cliente configurado con autenticación y logging
    session = requests.Session()
    session.auth = ("user", "pass")
    session.headers.update({"X-Env": "test"})
    session.timeout = 5
    yield session
    session.close()

def test_api_status(http_client):
    resp = http_client.get("https://api.service.local/health")
    assert resp.status_code == 200
```

**Uso en DevOps:**

* En la fase de **Integration Tests**, `http_client` puede apuntar a un servicio mockeado localmente o a un contenedor Docker levantado por el pipeline.
* En **Acceptance/E2E**, configuramos `http_client` para que use la URL de staging, simplemente cambiando una variable de entorno (sin modificar el test).


#### Setter-like fixtures

**Descripción:**
En lugar de devolver instancias completas, estos fixtures exponen funciones u objetos de utilidad que permiten parchear o ajustar dinámicamente comportamientos, tanto del código bajo prueba como de dependencias globales o módulos.

**Características clave:**

* **Flexibilidad puntual:** el fixture ofrece un "setter" o un contexto que modifica el estado durante el test, ideal para simular fallos y escenarios de borde.
* **Monkepatch centralizado:** encapsula llamadas a `monkeypatch.setattr`, `monkeypatch.setenv` o substituciones de módulos completos, evitando código repetido en cada test.
* **Scope reducido:** normalmente scope `function`, pues cada test puede requerir parches distintos.

**Ejemplo (pytest con monkeypatch):**

```python
import pytest
from myapp import servicio_pago

@pytest.fixture
def patch_gateway(monkeypatch):
    # Provee una función para sobrescribir el cliente de pagos
    def _patch(success=True):
        class FakeGateway:
            def procesar(self, monto):
                if success:
                    return {"status": "ok"}
                else:
                    raise Exception("Falló conexión al gateway")
        monkeypatch.setattr(servicio_pago, "Gateway", FakeGateway)
    return _patch

def test_pago_exitosa(patch_gateway):
    patch_gateway(success=True)
    resultado = servicio_pago.realizar_pago(100)
    assert resultado["status"] == "ok"

def test_pago_fallido(patch_gateway):
    patch_gateway(success=False)
    with pytest.raises(Exception):
        servicio_pago.realizar_pago(100)
```

**Uso en DevOps:**

* Durante pruebas unitarias, `patch_gateway` simula comportamientos del gateway de pago sin necesidad de un entorno real ni de credenciales.
* En un pipeline paralelo, varios tests aplican diversos parches, permitiendo comprobar la lógica de recuperación ante errores en escenarios controlados.


#### Interface-driven fixtures

**Descripción:**
Estos fixtures proporcionan implementaciones mínimas (fakes o stubs) que satisfacen únicamente la interfaz pública esperada por la lógica de negocio. No cargan librerías pesadas ni conocen detalles internos, lo que acelera la ejecución y refuerza el principio de Liskov Substitution.

**Características clave:**

* **Ligereza extrema:** al limitarse a métodos stub con comportamiento controlado, consumen muy pocos recursos.
* **Aislamiento completo:** no requieren conexiones externas, bases de datos ni servicios.
* **Documentación implícita:** el stub deja claro qué métodos e interacciones son relevantes para el test.

**Ejemplo (pytest):**

```python
import pytest
from typing import Protocol

# Definición de la interfaz (en Python 3.8+ via Protocol)
class Repositorio(Protocol):
    def guardar(self, entidad): ...
    def buscar(self, id): ...

@pytest.fixture
def repo_fake():
    class RepositorioFake:
        def __init__(self):
            self.almacen = {}
        def guardar(self, entidad):
            self.almacen[entidad.id] = entidad
        def buscar(self, id):
            return self.almacen.get(id)
    return RepositorioFake()

def test_creacion_entidad(repo_fake):
    servicio = ServicioEntidades(repo=repo_fake)
    entidad = Entidad(id=1, valor="X")
    servicio.crear(entidad)
    assert repo_fake.buscar(1).valor == "X"
```

**Uso en DevOps:**

* En **Unit Tests**, `repo_fake` permite verificar toda la lógica de `ServicioEntidades` sin arrancar una base de datos real.
* Al promover el uso de Protocols o interfaces explícitas, se facilita la migración a un stub con un contenedor de Redis en una fase de integración, simplemente cambiando la fixture.

####  Integración de DI en pipelines

#### Etapa de pruebas unitarias: máxima velocidad

* **Fixtures empleadas:** Setter-like e Interface-driven
* **Objetivo:** aislar la lógica de negocio y validar cada unidad con stubs y mocks ultraligeros.
* **Estrategia DevOps:** ejecutar estos tests en cada commit, aprovechando runners efímeros con capas de caché para dependencias, asegurando feedback en segundos.

**Ejemplo de pipeline:**

```yaml
stages:
  - unit_test

unit_test:
  stage: unit_test
  script:
    - pytest tests/unit --maxfail=1 --disable-warnings -q
  tags:
    - fast
```

#### Etapa de pruebas de integración: realismo controlado

* **Fixtures empleadas:** Constructor-like (con containers) y Setter-like para ajustes puntuales.
* **Objetivo:** verificar interacciones entre componentes (DB, colas, servicios externos).
* **Estrategia DevOps:** emplear Docker Compose o Kubernetes ephemeral namespaces para levantar servicios; reutilizar fixtures con configuración alternativa.

**Ejemplo de pipeline:**

```yaml
stages:
  - integration_test

integration_test:
  stage: integration_test
  services:
    - postgres:13
    - rabbitmq:3
  variables:
    DB_HOST: postgres
    MQ_HOST: rabbitmq
  script:
    - pytest tests/integration --docker-compose docker-compose.test.yml
```

En este contexto, el fixture `db_tmp` (Constructor-like) detecta la variable `DB_HOST` y conecta al contenedor levantado por el pipeline, mientras `patch_gateway` (Setter-like) puede simular puntos débiles en el flujo de mensajes.

####  Reutilización de código de test

Gracias a la abstracción mediante fixtures, el **mismo conjunto de tests** —idénticas funciones y aserciones— puede correr tanto en la etapa rápida de unit tests como en la más completa de integration tests. Solo cambia la configuración de los fixtures:

* **Mode local (unit):** los fixtures de integración devuelven stubs e interfaces, reduciendo latencia.
* **Mode CI (integration):** esos mismos fixtures detectan flags de entorno (`CI=true`) y devuelven instancias conectadas a contenedores Docker o servicios reales de staging.

```python
@pytest.fixture
def repo(request):
    if request.config.getoption("--mode") == "unit":
        return RepositorioFake()
    else:
        uri = f"postgresql://{os.getenv('DB_HOST')}/test"
        return RepositorioReal(uri)
```

En el pipeline:

* **Unit tests:** `pytest --mode unit`
* **Integration tests:** `pytest --mode integration`

####  Flexibilidad y mantenimiento

* **Escalabilidad de la suite:** añadir nuevas variantes de fixtures (por ejemplo, para un nuevo microservicio) no obliga a modificar tests anteriores.
* **Aislamiento de entornos:** las mismas pruebas pueden ejecutarse en local, en contenedores CI y en staging, sin duplicar código.
* **Visibilidad y control:** errores en unit tests señalan problemas de lógica pura; errores en integration tests advierten de incompatibilidades de infraestructura o configuración.


La combinación de **Constructor-like**, **Setter-like** e **Interface-driven fixtures**, unida a una orquestación inteligente en el pipeline de CI/CD, permite a los equipos DevOps alcanzar un equilibrio entre velocidad y realismo de las pruebas, garantizando un flujo de entrega continuo donde cada cambio sea validado de forma precisa, eficiente y reproducible.


