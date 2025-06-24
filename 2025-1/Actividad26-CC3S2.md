### Actividad: Implementación continua con GitHub Actions

Referencia para la actividad: [kapumota/Ejemplos-github-actions](https://github.com/kapumota/Ejemplos-github-actions).

### ¿Qué es la implementación continua?

#### Ejercicio teórico

* ¿Qué es GitHub Actions?
* Redacta una definición de "implementación continua" (≤150 palabras), diferenciándola de "entrega continua" y "despliegue continuo".
* Incluye un ejemplo de un proyecto Python (por ejemplo, un script `app.py` que escribas tú) donde al hacer `push` a `main` se publique
  automáticamente un paquete en PyPI de prueba.

#### Ejercicio práctico

* En la raíz del repo crea un script Python `deploy.py` que imprima:

  ```python
  # deploy.py
  print("Desplegando versión X.Y.Z en entorno de pruebas…")
  ```
* Modifica el workflow `.github/workflows/ci.yml` para que, al hacer push a `main`:

  1. Instale Python:

     ```yaml
     - name: Setup Python
       uses: actions/setup-python@v4
       with:
         python-version: "3.x"
     ```
  2. Ejecute `python deploy.py`.
* Verifica en Actions que veas la salida de tu script.

### ¿Por qué automatizar la implementación?

* Crea en el repo un archivo `Riesgos-Automatización.md` con una tabla que compare **3 ventajas** de un deploy automatizado vs **3 riesgos** de hacerlo manual, y propone contramedidas.

#### Ejercicio práctico

* Añade dos scripts en Python:

  * `deploy_manual.py` que pida input con `input("¿Confirmas deploy? (s/n): ")`.
  * `deploy_auto.py` que no pida nada y simule el deploy.
* Crea dos workflows:

  * `manual.yml` dispara en `push` pero falla si `deploy_manual.py` devuelve "n".
  * `auto.yml` dispara en `push` e invoca `deploy_auto.py`.
* Mide (cronómetro en mano) el tiempo de cada uno desde el push hasta fin de job.


### Introducción a la automatización con GitHub Actions

#### Ejercicio

* Abre `.github/workflows/ci.yml` y anota en un comentario junto a cada sección:

  * `name:` -> nombre del workflow.
  * `on:` -> eventos que lo disparan.
  * `jobs:` -> definición de jobs y runners.
  * Dentro de `steps`: diferencia entre `uses:` y `run:`.

#### Ejercicio práctico

* Crea un script Python `lint.py` que compruebe estilo (por ejemplo, use `flake8` desde código):

  ```python
  # lint.py
  import subprocess, sys
  result = subprocess.run(["flake8", "."], capture_output=True)
  print(result.stdout.decode(), file=sys.stderr)
  sys.exit(result.returncode)
  ```
* Crea `ci-lint.yml` que:

  1. Use `actions/setup-python@v4`.
  2. Instale `flake8` (`pip install flake8`).
  3. Ejecute `python lint.py`.
* Confirma que falla si introducimos una línea con PEP8 violado.


### ¿Por qué GitHub Actions?

#### Ejercicio de investigación

* Escribe en `Comparativa-CI.md` un párrafo donde compares GitHub Actions con **Jenkins** y **GitLab CI**, enfocándote en integración con GitHub, facilidad de uso y coste.

#### Ejercicio comparativo

* En el repo crea dos carpetas:

  * `.github-flows/` con tu `ci.yml`.
  * `jenkins-pipeline/` con un `Jenkinsfile` equivalente que llame a `index.sh` y a `deploy.py`.
* Documenta en el README las diferencias de sintaxis.

### ¿Qué es un flujo de trabajo?

#### Ejercicio conceptual

* Dibuja un diagrama ASCII en `diagrama-flujo.txt`:

  ```
  [push] -> [checkout] -> [setup-python] -> [build] -> [test] -> [deploy]
  ```

  y añade una breve leyenda explicando cada bloque.

#### Ejercicio práctico

* Modifica `ci.yml` para tener **2 jobs** paralelos:

  ```yaml
  jobs:
    build:
      runs-on: ubuntu-latest
      steps: ...
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - run: python -m unittest discover
    deploy:
      needs: [build, test]
      runs-on: ubuntu-latest
      steps:
        - run: python deploy.py
  ```
* Verifica en la pestaña Actions que `build` y `test` corren simultáneos y `deploy` espera a ambos.


### Creación de un nuevo flujo de trabajo

#### Ejercicio paso a paso

* Añade en el README un bloque "Cómo crear un workflow" con comandos:

  ```bash
  mkdir -p .github/workflows
  cat > .github/workflows/new-workflow.yml <<EOF
  name: Nuevo
  on: [push]
  jobs:
    dummy:
      runs-on: ubuntu-latest
      steps:
        - run: echo "¡Funciona!"
  EOF
  git add .
  git commit -m "Añadir nuevo workflow"
  git push
  ```
* Simula un error de indentación y describe cómo depurarlo leyendo el log de Actions.

#### Ejercicio práctico

* Si tienes la CLI de GitHub (`gh`), usa:

  ```bash
  gh workflow create
  ```

  y sigue el prompt para generar un template. Luego extrae el YAML generado a `.github/workflows/ci-from-cli.yml` y ajústalo.

###Invocación de comandos en línea

#### Ejercicio teórico

* Explica en `Usos-Run-vs-Uses.md` la diferencia entre `run: python script.py` y usar una acción del Marketplace como `actions/setup-python@v4`. ¿Cuándo conviene cada una?

#### Ejercicio práctico

* En tu `ci.yml` añade un paso:

  ```yaml
  - name: Compilar varios módulos
    run: |
      python -m compileall src/module1
      python -m compileall src/module2
  ```
* Comprueba que en la salida ves las rutas compiladas.


### Activación por cambio de código

#### Ejercicio práctico

* Ajusta `ci.yml` para que solo se dispare en cambios dentro de `src/`:

  ```yaml
  on:
    push:
      paths:
        - 'src/**'
  ```
* Haz commits de prueba en `docs/` y en `src/` y observa las diferencias en Actions.

#### Ejercicio de validación

* Documenta en `Pruebas-Paths.md` dos logs:

  * Uno donde no se lanza el workflow (cambio en `README.md`).
  * Otro donde sí (cambio en `src/hello.py`).

###Historial del flujo de trabajo

#### Ejercicio de exploración

* Accede a la pestaña **Actions** -> selecciona `CI` -> revisa todas las ejecuciones.
* Crea `Historial.md` anotando: número de ejecuciones, ramas y tiempos (más rápida vs más lenta).

#### Ejercicio práctico

* Añade este badge al README:

  ```md
  ![CI status](https://github.com/<TU_USUARIO>/Ejemplos-github-actions/actions/workflows/ci.yml/badge.svg)
  ```
* Provoca un fallo (mete un error de sintaxis en `deploy.py`) y confirma que el badge cambia a "failed".


### Activación manual desde la UI

#### Ejercicio práctico

* Crea `.github/workflows/dispatch.yml`:

  ```yaml
  name: Manual Dispatch
  on: workflow_dispatch
  jobs:
    run-python:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v4
        - run: python deploy.py
  ```
* Desde la pestaña **Actions**, pulsa "Run workflow" y observa cómo se ejecuta.

