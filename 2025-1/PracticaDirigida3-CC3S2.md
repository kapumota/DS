### Herramientas del shell

1 . Lee la ayuda de [man ls](https://www.man7.org/linux/man-pages/man1/ls.1.html) y escribe un comando `ls` que liste archivos de la siguiente manera:

- Incluye todos los archivos, incluidos los ocultos  
- Los tamaños aparecen en formato legible por humanos (p. ej. 454M en lugar de 454279954)  
- Los archivos se ordenan por fecha de modificación (del más reciente al más antiguo)  
- La salida está coloreada  

Un ejemplo de salida se vería así:

```text
-rw-r--r--   1 user group 1.1M Jan 14 09:53 f1
drwxr-xr-x   5 user group  160 Jan 14 09:53 .
-rw-r--r--   1 user group  514 Jan 14 06:42 f2
-rw-r--r--   1 user group 106M Jan 13 12:12 f3
drwx------+ 47 user group 1.5K Jan 12 18:08 ..
```

### Bash

> Guarda cada bloque en su correspondiente archivo, dale permisos con `chmod +x` y adáptalo a tu repositorio.

#### Paso 1 – Abrir la terminal y verificar Bash

1. Abre tu **Terminal** en Linux/macOS o Git Bash en Windows.  
2. Comprueba la versión de Bash:
   ```bash
   bash --version
   ```
3. Asegúrate de usar la cabecera portable en tus scripts:
   ```bash
   #!/usr/bin/env bash
   ```

#### Paso 2 – "Hello, World!": tu primer script

1. Crea `hello.sh`:
   ```bash
   nano hello.sh
   ```
2. Escribe:
   ```bash
   #!/usr/bin/env bash
   echo "Hello, World!"
   ```
3. Guarda y habilita:
   ```bash
   chmod +x hello.sh
   ```
4. Ejecútalo:
   ```bash
   ./hello.sh
   ```

#### Paso 3 – Asignación de variables

```bash
#!/usr/bin/env bash
NOMBRE="Cesar"
readonly PI=3.14159
export ENV="producción"

echo "Usuario: $NOMBRE"
echo "PI vale: $PI"
echo "Entorno: $ENV"
```

- Usa siempre comillas al expandir: `"$VAR"`.  
- Activa `set -u` para error si variable no definida.

#### Paso 4 – Parámetros posicionales

```bash
#!/usr/bin/env bash
# script_params.sh
echo "Script: $0"
echo "1er parámetro: $1"
echo "Todos: $@"
echo "Cantidad: $#"
shift 1
echo "Ahora \$1 es: $1"
```

Ejecuta:
```bash
./script_params.sh f1 f2 f3
```
#### Paso 5 – Arrays en Bash

```bash
#!/usr/bin/env bash
FRUTAS=(manzana banana cereza)
FRUTAS+=("durazno")

echo "Total frutas: ${#FRUTAS[@]}"
for f in "${FRUTAS[@]}"; do
  echo "Fruta: $f"
done

declare -A EDADES=([Alice]=28 [Kapu]=35)
echo "Kapu tiene ${EDADES[Kapu]} años"
```

#### Paso 6 – Expansiones

#### Aritmética

```bash
a=7; b=3
echo "$a + $b = $((a + b))"
echo "$a ** $b = $((a ** b))"
```

#### Substitución de comandos

```bash
fecha=$(date +%Y-%m-%d)
archivos=$(ls | wc -l)
echo "Hoy: $fecha, Archivos: $archivos"
```

#### Otras

```bash
VAR=""
echo "${VAR:-default}"       # default si VAR vacío
txt="archivo.tar.gz"
echo "${txt%.tar.gz}"        # quita sufijo
```

#### Paso 7 – Pipes y redirección

```bash
# stdout a archivo
ls -l > listado.txt
# stderr
grep foo *.log 2> errores.log
# ambos
make &> build.log
# pipe
ps aux | grep sshd | awk '{print $2}'
# process substitution
diff <(sort file1) <(sort file2)
```

#### Paso 8 – Condicionales

#### if

```bash
#!/usr/bin/env bash
num=$1
if [[ -z $num ]]; then
  echo "Pasa un número"
  exit 1
elif (( num % 2 == 0 )); then
  echo "$num es par"
else
  echo "$num es impar"
fi
```

#### case

```bash
#!/usr/bin/env bash
ext="$1"
case "$ext" in
  txt) echo "Texto" ;;
  sh)  echo "Shell" ;;
  py)  echo "Python" ;;
  *)   echo "Desconocido" ;;
esac
```

#### Paso 9 – Bucles

```bash
# for clásico
for ((i=1;i<=3;i++)); do echo "Iter $i"; done

# for-in
for file in *.sh; do echo "Script: $file"; done

# while
count=3
while (( count>0 )); do echo "$count"; ((count--)); done

# until
until [[ -f resultado.txt ]]; do sleep 1; done
echo "resultado.txt listo"
```

#### Paso 10 – Funciones

```bash
#!/usr/bin/env bash
saludar() {
  local name=$1
  echo "Hola, $name!"
}
saludar "Equipo"

dividir() {
  local a=$1 b=$2
  (( b==0 )) && return 1
  echo "$((a/b))"
}
if res=$(dividir 10 2); then
  echo "División: $res"
else
  echo "Error división"
fi
```

#### Paso 11 – Depuración

```bash
set -xe  # traza + salir al error
export PS4='+ ${BASH_SOURCE}:${LINENO}:${FUNCNAME[0]}: '
trap 'echo "Error en línea $LINENO"; exit 1' ERR
```
### **Ejercicios**


1 . Escribe funciones de Bash `marco` y `polo` que hagan lo siguiente: cada vez que ejecutes `marco`, debe guardarse de alguna manera el directorio de trabajo actual, luego, cuando ejecutes `polo`, sin importar en qué directorio te encuentres, `polo` te debe devolver (con `cd`) al directorio en el que ejecutaste `marco`.
   Para facilitar la depuración, puedes poner el código en un archivo `marco.sh` y recargarlo con `source marco.sh`.

2 . Tienes un comando que falla muy raramente. Para depurarlo necesitas capturar su salida, pero puede llevar tiempo que falle. Escribe un script de Bash que ejecute el siguiente fragmento **hasta que falle**, capture sus flujos de salida estándar y de error en archivos, y finalmente imprima todo:

```bash
#!/usr/bin/env bash

n=$(( RANDOM % 100 ))

if [[ n -eq 42 ]]; then
   echo "Algo esta pasando!"
   >&2 echo "El error fue por usar numero magicos"
   exit 1
fi

echo "Todo salio de acuerdo al plan"
```
Indica cuántas ejecuciones fueron necesarias para que ocurriera el fallo.

3 . El `-exec` de `find` puede ser muy poderoso para realizar operaciones sobre los archivos que encuentra. Sin embargo, ¿qué pasa si queremos hacer algo con **todos** los archivos, como crear un archivo ZIP? Algunos comandos leen de **STDIN**, pero otros (como `tar`) necesitan recibir la lista de archivos como argumentos. Para unir ambos mundos tenemos `xargs`, que ejecuta un comando tomando su **STDIN** como lista de argumentos. Por ejemplo:

```bash
ls | xargs rm
```

eliminará los archivos que `ls` lista.

**Tu tarea**: escribe un comando que encuentre **de manera recursiva** todos los archivos HTML en una carpeta y los comprima en un ZIP. Ten en cuenta que debe funcionar aunque los nombres de archivo contengan espacios (pista: revisa la opción `-d` o usa `-print0` en `find` junto con `-0` en `xargs`).

4 . Escribe un comando o script que, de forma recursiva, encuentre el archivo **más recientemente modificado** en un directorio. Y, más en general, ¿puedes listar todos los archivos por orden de recencia?

#### Paso 12 – Expresiones regulares en Bash

```bash
#!/usr/bin/env bash
email="$1"
re='^[[:alnum:]_.+-]+@[[:alnum:]-]+\.[[:alnum:].-]+$'
if [[ $email =~ $re ]]; then
  echo "Email válido"
  echo "Usuario: ${BASH_REMATCH[1]}"  # primer grupo
else
  echo "Email inválido"
fi
```
#### Paso 13 – Expresiones regulares en Python

Crea `extract_emails.py`:

```python
#!/usr/bin/env python3
import re, sys
texto=sys.stdin.read()
pat=re.compile(r'([A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+)')
for email in set(pat.findall(texto)):
    print(email)
```

Uso:
```bash
cat logs.txt | python3 extract_emails.py
```

**Validar nombre de rama**

```bash
#!/usr/bin/env bash
branch=$(git rev-parse --abbrev-ref HEAD)
# solo: feature/XYZ-123-descripcion o hotfix/XYZ-123
re='^(feature|hotfix)\/[A-Z]{2,5}-[0-9]+-[a-z0-9]+(-[a-z0-9]+)*$'
if [[ ! $branch =~ $re ]]; then
  echo "Nombre de rama inválido: $branch"
  echo "Formato correcto: feature/ABC-123-descripcion"
  exit 1
fi
```

**Validar mensaje de commit**

```bash
#!/usr/bin/env bash
msg_file=$1
# tipo(scope)!?: descripción de al menos 10 caracteres
re='^(feat|fix|docs|style|refactor|perf|test|chore)(\([a-z0-9_-]+\))?(!)?: .{10,}$'
if ! grep -Eq "$re" "$msg_file"; then
  echo "Mensaje de commit no cumple conventional commits"
  echo "Ej: fix(parser): manejar comillas dobles correctamente"
  exit 1
fi
```

**Validar formato de tag semántico**

```bash
#!/usr/bin/env bash
tag="$1"
# vX.Y.Z o X.Y.Z-prerelease+metadata
re='^v?[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$'
if [[ ! $tag =~ $re ]]; then
  echo "Tag inválido: $tag"
  echo "Formato semver: 1.2.3, v1.2.3-beta+exp"
  exit 1
fi
```

**Extraer issue IDs de mensajes (`git log`)**

```bash
git log --oneline | \
  grep -Po '(?<=\[)[A-Z]{2,5}-[0-9]+(?=\])' | sort -u
# Explicación:
# (?<=\[)  ─ lookbehind para "["
# [A-Z]{2,5}-[0-9]+  ─ proyecto-1234
# (?=\])   ─ lookahead para "]"
```

**Detectar merges automáticos y extraer la rama objetivo**

```bash
git log --grep='^Merge branch' --pretty=format:'%s' | \
  grep -Po '(?<=Merge branch ')[^']+' 
# Captura el nombre de la rama tras "merge branch '<rama>'"
```
**Paso con grupo nombrado y alternancia**

```python
from behave import given

@given(r'^(?P<user>[A-Za-z0-9_]+) tiene (?P<count>[0-9]+) (artículos|productos)$')
def step_user_items(context, user, count):
    # user: nombre de usuario
    # count: número de artículos o productos
    context.user = user
    context.count = int(count)
```

**Paso con partes opcionales y lookahead**

```python
from behave import when

@when(r'^el usuario intenta(?: iniciar sesión(?: con contraseña "(?P<pw>[^"]+)")?)?$')
def step_login_optional_pw(context, pw=None):
    # El paso coincide con:
    #   "el usuario intenta"
    #   "el usuario intenta iniciar sesión"
    #   'el usuario intenta iniciar sesión con contraseña "abc"'
    context.pw = pw
```

**Validar formatos de fecha dentro de un paso**

```python
from behave import then

@then(r'^la fecha de entrega es (?P<date>\d{4}-\d{2}-\d{2})$')
def step_check_date(context, date):
    # date: "2025-04-16"
    import datetime
    datetime.datetime.strptime(date, '%Y-%m-%d')
```

**Step definition para comandos Git**

```python
from behave import given

@given(r'^estoy en la rama "(?P<branch>[a-z0-9/_-]+)"$')
def step_on_branch(context, branch):
    import subprocess
    current = subprocess.check_output(['git','rev-parse','--abbrev-ref','HEAD']).decode().strip()
    assert current == branch
```

**Capturar tablas Gherkin con regex dinámico**

```python
from behave import then
import re

@then(r'^los siguientes usuarios:$')
def step_table_users(context):
    # context.table tendrá filas:
    # | user   | age |
    # | alice  | 30  |
    # Validación adicional:
    for row in context.table:
        assert re.match(r'^[a-z]+$', row['user'])
        assert re.match(r'^[0-9]{1,3}$', row['age'])
```

**Scenario outline con ejemplos que usan regex**

```gherkin
Scenario Outline: Validación de correos
  Given el email "<email>"
  When valido el formato
  Then debe ser <valid>

Examples:
  | email                 | valid  |
  | user@example.com      | True   |
  | invalid-email@        | False  |
  | otra.cosa@dominio.org | True   |
```

```python
from behave import given, then
import re

EMAIL_RE = re.compile(r'^[[:alnum:]_.+-]+@[[:alnum:]-]+\.[[:alnum:].-]+$')

@given(r'el email "(?P<email>[^"]+)"')
def step_set_email(context, email):
    context.email = email

@then(r'debe ser (?P<valid>True|False)')
def step_check_email(context, valid):
    match = bool(EMAIL_RE.match(context.email))
    assert match == (valid == 'True')
```

#### Paso 14 – BDD con `behave`

1. **Feature** (`features/login.feature`):
   ```gherkin
   Feature: Login
     Scenario Outline: credenciales válidas
       Given el usuario "<user>" con contraseña "<pass>"
       When intenta iniciar sesión
       Then debe ver "Bienvenido, <user>"

     Examples:
       | user  | pass    |
       | alice | secret1 |
   ```
2. **Steps** (`features/steps/login_steps.py`):
   ```python
   from behave import given, when, then
   from myapp.auth import autenticar

   @given(r'el usuario "(?P<user>[^"]+)" con contraseña "(?P<pass>[^"]+)"')
   def step_user(c, user, pass_):
       c.user, c.passwd = user, pass_

   @when('intenta iniciar sesión')
   def step_try(c):
       c.result = autenticar(c.user, c.passwd)

   @then(r'debe ver "(?P<msg>[^"]+)"')
   def step_verify(c, msg):
       assert c.result == msg
   ```
3. Ejecuta:
   ```bash
   behave -q
   ```
#### Paso 15 – Pipelines CI

**GitHub actions** (`.github/workflows/ci.yml`):

```yaml
name: CI
on: [push,pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with: python-version: 3.10
      - run: pip install -r requirements.txt
      - run: pytest -q
      - run: behave -q
```

**Makefile local**:

```makefile
.PHONY: lint test bdd all
lint:
    flake8 src tests
test:
    pytest -q
bdd:
    behave -q
all: lint test bdd
```

**Problema 1: Script de limpieza de ramas y atashes en Git**

Construye un script Bash llamado `clean_git.sh` que automatice la limpieza de ramas locales y remotas y gestione stashes de  forma interactiva, aplicando exclusivamente los conceptos de variables, parámetros posicionales, arrays, expansiones, pipes, 
condicionales, bucles, funciones y depuración vistos en el tutorial.

**Pasos**

1. El script debe comenzar con `#!/usr/bin/env bash` y activar `set -euo pipefail` para robustez.  
2. Define una función `mostrar_ayuda` que imprima el uso esperado y las opciones disponibles (por ejemplo, `--help`, `--branches`, `--stashes`).  
3. Utiliza un parámetro posicional (`$1`) para determinar la acción:  
4. Si el usuario pasa `--branches`, invocar la función `limpiar_ramas`.  
5. En `limpiar_ramas`, solicita al usuario un patrón de expresión regular para filtrar ramas locales (por ejemplo, `feature/.*` o `bugfix/.*`).  
6. Valida la entrada con `[[ $patron =~ ^[[:alnum:]_/.-]+$ ]]`; en caso de fallo, mostrar un error y salir.  
7. Lista las ramas locales que coincidan usando `git branch | grep -E "$patron"` y almacenar el resultado en un array Bash.  
8. Si el array está vacío, informa "No hay ramas que coincidan con $patron" y regresar al menú.  
9. Itera sobre el array con un bucle `for` y, para cada rama, preguntar “¿Eliminar rama <nombre>? (s/n)”.  
10. Lee la respuesta con `read -r` y usa un condicional `if [[ $respuesta =~ ^[sS]$ ]]` para eliminarla (`git branch -D`).  
11. Tras procesar locales, lista ramas remotas coincidentes (`git branch -r | grep -E "$patron"`), y repetir el mismo proceso (usando `git push origin --delete`).  
12. Crea una función `gestionar_stashes` que, al recibir `--stashes`, liste los stashes con índices (`git stash list | nl -w2 -s'. '`), capturándolo en una variable.  
13. Solicita al usuario una lista de índices separados por espacios (por ejemplo, “0 2 4”).  
14. Valida cada índice con `[[ $i =~ ^[0-9]+$ ]]`; si algún índice no es válido, abortar con mensaje de error.  
15. Convierte la línea de índices en un array Bash y recorrerlo con un `for`.  
16. Para cada índice, pide la confirmación antes de aplicar (`git stash apply stash@{$i}`) o eliminar (`git stash drop stash@{$i}`), según la opción inicial (push o pop).  
17. Añade una función `backup_reflog` que, al pasar `--backup`, guarde el reflog en un archivo nombrado `reflog_$(date +%Y%m%d_%H%M%S).log`.  
18. Usa redirecciones (`>`) y pipes para filtrar entradas del reflog que contengan "reset" o "merge".  
19. Incorpora una función `informe_json` que genere un JSON con:  
    - Nombre de la rama actual (`git rev-parse --abbrev-ref HEAD`).  
    - Cantidad de stashes (`git stash list | wc -l`).  
    - Lista de tags (`git tag | jq -R -s -c 'split("\n")[:-1]'`).  
    - Submódulos (`git submodule status | awk '{print $2}' | jq -R -s -c 'split("\n")[:-1]'`).  
20. Utiliza here-documents para ensamblar el JSON dentro de una variable Bash.  
21. Imprime el JSON con `echo "$json"` y redirigir a `informe_$(date +%Y%m%d).json`.  
22. Todas las funciones deben documentarse mediante comentarios previos con `#`.  
23. Al final, implementa un `case $1 in … esac` para enrutar las opciones (`--branches`, `--stashes`, `--backup`, `--report`, `--help`).  
24. Añade un `else` que muestre la ayuda si la opción no coincide.  
25. Incluir una regla de depuración: si se pasa `--debug`, activar `set -x` y exportar `PS4='+ ${BASH_SOURCE}:${LINENO}:${FUNCNAME[0]}: '`.  
26. Prueba el script dentro de un repositorio con varias ramas y stashes, verificando que los arrays y bucles funcionan correctamente.  
27. Documenta en un README los comandos de uso y ejemplos de ejecución.    

**Problema 2 : Hook Pre‑Commit y generador de reporte en Bash**  
Implementa un hook `pre-commit` en Bash que ejecute una serie de comprobaciones y, en caso de éxito, lance un script de generación de reporte del estado del repositorio, aplicando exclusivamente variables, arrays, loops, condicionales, expansiones y funciones de Bash.

1. Crea el archivo `.git/hooks/pre-commit` con `#!/usr/bin/env bash` y permisos `chmod +x`.  
2. Al inicio del hook, activa `set -euo pipefail` y documenta el propósito del hook con comentarios.  
3. Define una función `check_todo_comments` que:  
   - Recoja en un array los archivos staged (`git diff --cached --name-only --diff-filter=ACM`).  
   - Filtre solo los que terminen en `.sh`, `.py` o `.js` usando `grep -E '\.(sh|py|js)$'`.  
   - Para cada archivo, busque líneas con `TODO` o `FIXME` usando `grep -En '(TODO|FIXME)'`.  
   - Si se encuentran coincidencias, las almacene en una variable `has_errors=true` y acumule los mensajes en un array `errors[]`.  
   - Al final, si `has_errors` es `true`, imprime todos los errores y sale con código 1.  
4. Define una función `run_shellcheck` que:  
    - Itere sobre los mismos archivos `.sh` y ejecute `shellcheck`.  
    - Si falla, captura la salida en una variable y marca `has_errors=true`.  
5. Define una función `run_pyflakes` que:  
    - Itere sobre archivos `.py` y ejecute `pyflakes`.  
    - Si hay warning o errores, los almacene  en el array `errors[]`.  
6. Define una función `generate_report` que:  
    - Cree un archivo `precommit_report_$(date +%Y%m%d_%H%M%S).txt`.  
    - Escriba en él:  
      -- Nombre de la rama actual (`git rev-parse --abbrev-ref HEAD`).  
      -- Lista de archivos staged.  
      -- Resultado de `git status --short`.  
      -- Mensajes de errores de `errors[]` separados por líneas.  
    - Muestra un mensaje al usuario: "Reporte generado en <ruta>".  
7. En el cuerpo principal del hook:  
    - Llamar a `check_todo_comments`, `run_shellcheck` y `run_pyflakes` en secuencia.  
    - Si `has_errors` es `true`, imprime "Commit abortado por errores" y salir con código 1.  
    - Si no hay errores, llamar a `generate_report` y permitir el commit.  
8. Incluye un condicional que, si se pasa la bandera `--skip-report`, solo realice las comprobaciones y no genere el reporte.  
9. Añade un bloque `trap` que en caso de cualquier error imprima "Error en hook pre-commit en la línea $LINENO" antes de salir.  
10. Documenta cada función y paso con comentarios claros.  
11. Prueba el hook en un repositorio con archivos Bash, Python y C++, confirmando que se comporta como se espera ante múltiples escenarios (TODOs detectados, scripts con errores de sintaxis, commits limpios).  
12. Incluye en el repositorio un archivo `HOOKS_README.md` con instrucciones de instalación y ejemplos de uso del hook.

**Problema 3: Generador de documentación automático**  

**Contexto:** Cada vez que se añade o modifica un docstring en un archivo Python, quieres generar automáticamente un sitio estático de documentación.  
1. Crea un hook `post-commit` que:  
   - Escanee los cambios en `.py` buscando docstrings multilínea con regex avanzadas (capturar `""" ... """`).  
   - Extraiga el módulo, la clase y la firma de la función junto al docstring.  
   - Pase esta información a un script generador (mockeable) que cree páginas Markdown.  
2. Plantea un Feature Gherkin con escenarios para:  
   - Interpretar docstrings con ejemplos de código enriquecido.  
   - Manejar funciones anidadas y métodos estáticos.  
   - Ignorar docstrings marcados con `@internal`.  
3. Implementa los steps en Behave usando Python y regex avanzadas (`re.DOTALL`, lookaround) para extraer correctamente toda la sección de docstring.  
4. Desarrolla pruebas Pytest parametrizadas para:  
   - Docstrings que contienen comillas triples anidadas.  
   - Casos límites: funciones sin docstrings deben ser ignoradas sin error.

