### Uso de Make en flujos DevOps con pytest y fixtures

Referencia: [Archivo makefile ](https://github.com/kapumota/DS/blob/main/2025-1/Actividades10-16-CC3S2/Makefile)

#### 1. Contexto y motivación

En entornos de desarrollo modernos, la colaboración estrecha entre equipos de desarrollo (Dev) y operaciones (Ops) —comúnmente denominada DevOps— exige automatizar tareas rutinarias con el fin de garantizar:

- **Reproducibilidad**: Que cualquier miembro del equipo pueda ejecutar los mismos comandos y obtener resultados idénticos.  
- **Eficiencia**: Minimizar errores humanos y acelerar los ciclos de retroalimentación.  
- **Calidad del código**: Detectar defectos lo más temprano posible mediante pruebas automatizadas y análisis estático.  
- **Visibilidad**: Registros claros de ejecución y reportes consolidados para seguimiento y auditoría.  

El uso de un **Makefile** aporta un punto de entrada estandarizado y declarativo, facilitando la orquestación de comandos complejos y promoviendo la documentación viva del proyecto. A continuación se detalla cómo este Makefile específico satisface los requisitos de DevOps y de un flujo de pruebas basado en pytest y fixtures.

#### 2. Diseño general del Makefile  

El Makefile se estructura en tres bloques principales:

1. **Variables de entorno y configuración**  
2. **Definición de objetivos (targets)**  
3. **Reglas de ejecución de cada objetivo**  

Este diseño modular permite:
- Centralizar parámetros ajustables (por ejemplo, `ACTIVITY`)  
- Documentar comandos cotidianos (`help`)  
- Describir flujos de instalación, linting, pruebas, cobertura y limpieza.  

#### 2.1 Variables de entorno

```make
# Actividad por defecto
ACTIVITY ?= aserciones_pruebas

# Lista de las actividades disponibles
ACTIVITIES = aserciones_pruebas coverage_pruebas factories_fakes objects_mocking \
             practica_tdd pruebas_fixtures pruebas_pytest
```

- **ACTIVITY**: Permite al usuario invocar `make test ACTIVITY=<nombre>` para focalizarse en un subdirectorio concreto de pruebas.  
- **ACTIVITIES**: Lista exhaustiva de todas las carpetas de actividades, fundamental para bucles en `test_all` y `coverage_individual`.  

La sintaxis `?=` habilita un valor por defecto que puede ser sobrescrito desde la línea de comando, promoviendo flexibilidad.


#### 3. Documentación integrada (`help`)

```make
.PHONY: help
help:
	@echo "Uso: make [comando] [opciones]"
	...
	@echo "Actividades disponibles:"
	@echo "  $(ACTIVITIES)"
```

- **`.PHONY`**: Evita colisiones con archivos que tengan el mismo nombre.  
- **`@`**: Suprime el eco del propio comando, dejando solo la salida deseada.  
- **Estructura**: Muestra de forma clara los comandos y opciones, convirtiendo al Makefile en una ayuda interactiva.

De esta forma, cualquier miembro del equipo puede ejecutar `make help` y conocer al instante el conjunto de acciones disponibles, mejorando la accesibilidad para nuevos integrantes.

#### 4. Instalación de dependencias

```make
.PHONY: install
install:
	@echo "Instalando dependencias..."
	pip install -r requirements.txt
```

- **Objetivo**: Garantizar que el entorno local (o virtual) contiene las librerías necesarias.  
- **DevOps**: En pipelines CI/CD, este target suele invocarse dentro de contenedores o agentes de build para preparar el entorno antes de compilar o testear.  
- **Recomendación**: Complementar con `pip install --upgrade pip` o entornos virtuales dedicados (venv, poetry, pipenv) para aislar dependencias.


#### 5. Análisis estático de código (`lint`)

```make
.PHONY: lint
lint:
	@echo "Ejecutando flake8..."
	flake8 .
```

- **flake8**: Herramienta que combina PyFlakes (errores de sintaxis y variables no usadas) y pep8 (estilo de código).  
- **Integración**: Se puede expandir con `black --check` para formateo o `mypy` para chequeo estático de tipos.  
- **Automatización**: En entornos CI, este objetivo es crítico para bloquear merges si aparecen errores de estilo o calidad.

#### 6. Ejecución de pruebas con pytest  

#### 6.1 Pruebas por actividad

```make
.PHONY: test
test:
	@echo "Ejecutando pruebas en la actividad: $(ACTIVITY)"
	cd Actividades/$(ACTIVITY) && \
	  PYTHONWARNINGS="ignore::DeprecationWarning" pytest .
```

- **Cambio de directorio**: Facilita agrupar tests por carpetas según la temática: aserciones, coverage, factories, etc.  
- **PYTHONWARNINGS**: Suprime warnings de deprecated, manteniendo salida limpia.  
- **pytest .**: Ejecuta todos los tests en la carpeta.  

Este enfoque:
- Mejora la **granularidad** de la ejecución de pruebas.  
- Permite al desarrollador enfocarse en un área de interés sin ejecutar todo el conjunto cada vez.

#### 6.2 Pruebas en todas las actividades

```make
.PHONY: test_all
test_all:
	@echo "Ejecutando pruebas en TODAS las actividades..."
	@for activity in $(ACTIVITIES); do \
	   echo "=========================================="; \
	   ... \
	   cd Actividades/$$activity && \
	     PYTHONWARNINGS="ignore::DeprecationWarning" pytest . || exit 1; \
	   cd - >/dev/null; \
	done
```

- **Bucle `for`**: Itera sobre la lista `ACTIVITIES`, ejecuta pytest en cada una y detiene la ejecución si alguna falla (`|| exit 1`).  
- **Separadores visuales**: Clarifican en la salida log el inicio de cada conjunto de tests.  
- **`cd - >/dev/null`**: Regresa al directorio original y suprime la ruta en la salida, manteniendo limpieza.

Este mecanismo es idóneo para pipelines de integración: con un solo comando se verifica todo el espectro de pruebas, bloqueando el pipeline si alguna falla.

#### 7. Medición de cobertura de código

#### 7.1 Cobertura unificada (`coverage`)

Aunque en el Makefile mostrado no existe un objetivo `coverage` independiente, es habitual definir:

```make
.PHONY: coverage
coverage:
	coverage run --source=. -m pytest && \
	coverage report -m && \
	coverage html
```

- **`coverage run`**: Ejecuta pytest bajo el módulo coverage, recopilando métricas de líneas ejecutadas.  
- **`--source=.`**: Especifica el directorio a instrumentar.  
- **`coverage report -m`**: Muestra porcentaje de cobertura por archivo.  
- **`coverage html`**: Genera reporte visual en HTML.

#### 7.2 Cobertura individual por actividad

```make
.PHONY: coverage_individual
coverage_individual:
	@echo "Ejecutando cobertura individual..."
	@for activity in $(ACTIVITIES); do \
	   echo "Generando cobertura para $$activity"; \
	   cd Actividades/$$activity && \
	   coverage erase && \
	   PYTHONWARNINGS="ignore::DeprecationWarning" \
	     coverage run --source=. -m pytest . && \
	   coverage report -m && \
	   coverage html -d htmlcov_$$activity || exit 1; \
	   cd - >/dev/null; \
	done
```

- **`coverage erase`**: Limpia datos previos de ejecución, garantizando resultados frescos.  
- **Directorio HTML por actividad**: Permite análisis granular de cobertura en cada módulo, ideal para equipos responsables de componentes específicos.

#### 8. Limpieza de artefactos (`clean`)

```make
.PHONY: clean
clean:
	@echo "Eliminando archivos de caché y reportes..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov htmlcov_*
	coverage erase
	@echo "Limpieza completa."
```

- **Eliminar cachés y reportes**: Evita interferencias de ejecuciones previas.  
- **`coverage erase`**: Borra datos de cobertura.  
- **Importancia**: En entornos de build limpios (contenedores efímeros) puede no ser necesario, pero localmente acelera reinicios.


#### 9. Integración de fixtures en pytest

El Makefile proporciona targets que ejecutan pytest. Para explotar al máximo pytest:

- **Definición de fixtures**: Se definen en `conftest.py` a nivel de proyecto o en cada carpeta de actividad. Permiten compartir datos de prueba, clientes de API simulados o conexiones a base de datos falsas.  
- **Mocks y fakes**: Agrupados en `factories_fakes`, se pueden usar fixtures parametrizadas para generar múltiples escenarios con mínima duplicación de código.  
- **Patrones de uso**:
  - `@pytest.fixture(scope="session")`: Cadena de vida de toda la suite.  
  - `@pytest.fixture(autouse=True)`: Se inyecta automáticamente en cada test, útil para configuración global.  
  - `@pytest.mark.usefixtures("mi_fixture")`: Para tests que requieren setup pero no consumen directamente la fixture.  

El uso sistemático de fixtures:

1. **Reduce duplicación** de setup/teardown.  
2. **Mejora legibilidad** al abstraer complejidad.  
3. **Facilita parametrización** para probar múltiples casos de entrada/salida.  


#### 10. Buenas prácticas DevOps y Make

1. **Idempotencia**: Cada target debe poder ejecutarse múltiples veces sin efectos secundarios no deseados.  
2. **Verbosidad ajustable**: Uso de variables como `VERBOSE=1` para alternar entre salidas silenciosas y detalladas.  
3. **Paralelismo**: Aprovechar `make -j` para ejecutar independentemente `test_all` y `coverage_individual`.  
4. **Entornos aislados**: Integrar con Docker o entornos virtuales:
   ```make
   .PHONY: docker-test
   docker-test:
       docker build -t miapp:dev .
       docker run --rm miapp:dev make test_all
   ```
5. **Control de errores**: Usar `set -e` en scripts shell invocados desde Make para detenerse ante el primer fallo.  
6. **Variables parametrizables**: Exponer rutas, versiones de Python (`PYTHON=python3.9`), directorios de artefactos (`REPORT_DIR=reports`).  


#### 11. Integración en pipelines CI/CD

Para integrar este Makefile en servicios como **GitHub Actions**, **GitLab CI** o **Jenkins**:

1. **Workflow de GitHub Actions** (`.github/workflows/ci.yml`):
   ```yaml
   name: CI
   on: [push, pull_request]
   jobs:
     build-test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Set up Python
           uses: actions/setup-python@v2
           with: python-version: '3.9'
         - name: Install dependencies
           run: make install
         - name: Lint code
           run: make lint
         - name: Run all tests
           run: make test_all
         - name: Coverage report
           run: make coverage
         - name: Upload coverage
           uses: codecov/codecov-action@v1
   ```
2. **Notificaciones**: En caso de fallo, los servicios envían alertas por correo o Slack.  
3. **Artefactos**: Publicar reportes HTML de cobertura como artefactos descargables.  


#### 12. Gestión de versiones y trazabilidad

- **Etiquetado**: Añadir un target `release` que cree un tag Git con el número de versión:
  ```make
  .PHONY: release
  release:
      @read -p "Versión (e.g., v1.0.0): " TAG; \
      git tag $$TAG && git push origin $$TAG
  ```
- **Changelog**: Generar un historial de cambios con `git log` en un archivo `CHANGELOG.md` automáticamente.  
- **Build reproducible**: Incluir `timestamp` y `commit hash` para identificación en reportes:
  ```make
  GIT_COMMIT := $(shell git rev-parse --short HEAD)
  BUILD_TIME := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
  ```


#### 13. Consideraciones de seguridad

1. **Variables de entorno sensibles**: Nunca incluir contraseñas o tokens en el Makefile. Usar `secrets` del CI para inyectarlas en tiempo de ejecución.  
2. **Dependencias confiables**: Auditar con `pip-audit` o `safety`.  
3. **Escaneo de vulnerabilidades**: Integrar objetivos adicionales como `make scan` que ejecuten OWASP Dependency-Check o Bandit.


#### 14. Integración de Git Hooks con Make

Para reforzar la calidad del código y automatizar chequeos antes de cada operación Git crítica, podemos combinar **Make** con **Git Hooks**. A continuación un ejemplo de configuración en `.git/hooks/pre-commit`:

```bash
#!/usr/bin/env bash
# pre-commit hook que invoca targets de Make

# 1. Linting: flake8 y black
echo "[pre-commit] Ejecutando lint..."
make lint || { echo "[pre-commit] Lint fallido. Abortando commit."; exit 1; }

# 2. Pruebas unitarias en el módulo principal
echo "[pre-commit] Ejecutando pruebas rápidas..."
make test ACTIVITY=pruebas_pytest || { echo "[pre-commit] Tests fallidos. Abortando commit."; exit 1; }

# 3. Análisis de seguridad (opcional)
# echo "[pre-commit] Escaneando vulnerabilidades..."
# make scan || { echo "[pre-commit] Vulnerabilidades detectadas. Abortando commit."; exit 1; }

echo "[pre-commit] Todo OK. Continuando con el commit."
exit 0
```

1. **Ubicación**: Copiar este script en `.git/hooks/pre-commit` y darle permisos `chmod +x`.  
2. **Targets usados**:
   - `make lint` incluye flake8 (y podría ampliarse con black/mypy).  
   - `make test` corre pytest en la carpeta de pruebas seleccionada.  
3. **Beneficios**:
   - **Bloqueo automático** de commits si fallan checks de estilo o pruebas.  
   - **Consistencia**: todos los desarrolladores aplican las mismas reglas antes de cada commit.  

#### 15. Uso de BDD con Behave y expresiones regulares

El enfoque de **Behavior-Driven Development (BDD)** con **behave** permite describir escenarios de negocio en lenguaje natural (Gherkin) y materializarlos en Python usando **regex** para step definitions. Podemos orquestar todo esto desde nuestro Makefile:

```make
.PHONY: bdd
bdd:
	@echo "Ejecutando BDD con behave..."
	cd features && behave --tags=@smoke --no-capture
```

#### 15.1 Estructura de directorios

```
.
├── features
│   ├── *.feature        # escenarios Gherkin
│   └── steps
│       └── steps.py     # definiciones de pasos
```

#### 15.2 Ejemplo de escenario Gherkin (`login.feature`)

```gherkin
# language: es
Feature: Autenticación de usuario
  Como usuario registrado
  Quiero iniciar sesión
  Para acceder a mi panel privado

  Scenario: Inicio de sesión exitoso
    Given un usuario con email "cesar@example.com" y contraseña "Secreto123"
    When intento iniciar sesión con email "cesar@example.com" y contraseña "Secreto123"
    Then debo ver el mensaje "Bienvenido, Cesar"
```

#### 15.3 Definición de pasos en `steps/steps.py`

```python
from behave import given, when, then
import re
from myapp.auth import authenticate, Session

@given(r'un usuario con email "(?P<email>[^"]+)" y contraseña "(?P<password>[^"]+)"')
def step_impl_crear_usuario(context, email, password):
    # Fixture: registra al usuario en base de datos de prueba
    context.user = {'email': email, 'password': password}
    Session.clear()
    Session.register(context.user)

@when(r'intento iniciar sesión con email "(?P<email>[^"]+)" y contraseña "(?P<password>[^"]+)"')
def step_impl_intentar_login(context, email, password):
    context.response = authenticate(email, password)

@then(r'debo ver el mensaje "(?P<mensaje>.+)"')
def step_impl_verificar_mensaje(context, mensaje):
    assert mensaje in context.response['message'], \
        f"Mensaje esperado '{mensaje}', obtenido '{context.response['message']}'"
```

- **Regex nombradas** (`?P<email>`, `?P<password>`) facilitan claridad en parámetros.  
- **Four Test Patterns** (ver sección siguiente) pueden aplicarse en cada step:  
  1. **Setup** (`@given`): preparar datos.  
  2. **Stimulus** (`@when`): ejecutar acción.  
  3. **Verify** (`@then`): comprobar resultado.  
  4. **Teardown** (automático al finalizar cada escenario en behave).


#### 16. Ciclo TDD y Four Test Patterns

Al combinar **TDD** con **Make** y pytest/behave, seguimos un flujo continuo de **Red→Green→Refactor** apoyado en los **Four Test Patterns**:

1. **Setup / Fixture**: preparar el estado inicial  
2. **Exercise / Stimulus**: invocar la función o flujo bajo prueba  
3. **Verify / Assertion**: comprobar que el comportamiento coincide con la expectativa  
4. **Teardown / Cleanup**: restaurar el entorno (suele gestionarlo pytest/behave)

#### 16.1 Flujo de trabajo con Make

```make
.PHONY: tdd
tdd:
	@echo "=== TDD ciclo: RED (falla) ==="
	pytest --maxfail=1 --disable-warnings -q && exit 1 || true
	@echo "=== GREEN (implementar) ==="
	# Aquí se espera que el desarrollador escriba el código necesario
	@echo "=== Re-ejecutar ==="
	pytest
	@echo "=== REFACTOR ==="
	# Momento de limpiar código, renombrar, mejorar cobertura
```

1. `make tdd` primero ejecuta tests, que deben **fallar** (Red).  
2. El desarrollador implementa la funcionalidad mínima para pasar tests (Green).  
3. Se vuelve a invocar `pytest` hasta que todos pasen.  
4. Finalmente, se refactoriza el código productivo sin alterar tests existentes.

#### 16.2 Ejemplo de test siguiendo Four Test Patterns

Archivo `test_calculadora.py`:

```python
import pytest
from calculadora import dividir

class TestDividir:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        # Setup: preparar posibles recursos
        yield
        # Teardown: no hay limpieza necesaria

    def test_division_entera(self):
        # Exercise
        resultado = dividir(10, 2)
        # Verify
        assert resultado == 5

    def test_division_por_cero(self):
        # Exercise & Verify consistente con excepción
        with pytest.raises(ZeroDivisionError):
            dividir(10, 0)
```

- **Setup**: la fixture `setup_teardown` podría inicializar registros, archivos temporales, etc.  
- **Exercise**: llamada a `dividir`.  
- **Verify**: uso de `assert` o `with pytest.raises`.  
- **Teardown**: implícito en pytest o en fixtures con `yield`.

#### 16.3 Integración de BDD y TDD

Para flujos híbridos, podemos definir otro target:

```make
.PHONY: ci
ci: lint test bdd coverage
```

De este modo, una única orden `make ci` realizará:

1. Linting  
2. Ejecución de todos los tests unitarios (TDD/pytest)  
3. Ejecución de escenarios BDD (behave)  
4. Generación de reportes de cobertura  

Así se cierra el ciclo completo de validación de calidad, desde tests de unidad hasta pruebas de aceptación de negocio.

