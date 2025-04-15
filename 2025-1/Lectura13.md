### 1. Hooks de Git

#### ¿Qué son los hooks de Git?

Los hooks son scripts (generalmente escritos en lenguajes de scripting como Bash, Python o Perl) que Git ejecuta automáticamente en respuesta a ciertos eventos o durante el  proceso de control de versiones. Se encuentran en el directorio `.git/hooks` de cada repositorio y permiten realizar diversas comprobaciones y automatizaciones en momentos  específicos, por ejemplo, antes de realizar un commit o después de hacer push.

Existen dos tipos principales de hooks:

- **Hooks del lado del cliente:** Se ejecutan en la máquina del desarrollador y se utilizan para realizar tareas locales, como validación de código o formateo automático antes del commit.
- **Hooks del lado del servidor:** Se utilizan en servidores remotos para acciones de integración continua, verificación de políticas o la aplicación de reglas de seguridad antes de aceptar cambios.

#### Ejemplos prácticos de hooks

##### **Pre-commit hook**

El hook `pre-commit` se ejecuta antes de que se realice un commit. Es muy útil para evitar que código defectuoso o que no cumpla con los estándares de calidad ingrese al repositorio. Por ejemplo, se puede implementar una comprobación de estilo o ejecutar pruebas unitarias para garantizar que el código pase ciertos criterios  antes de la confirmación.

**Ejemplo de un hook pre-commit en Bash:**

```bash
#!/bin/bash
# Script pre-commit: valida que no haya errores de sintaxis en archivos Python

# Lista de archivos añadidos o modificados que están siendo committeados
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

if [ -z "$FILES" ]; then
  exit 0
fi

PASS=true

for file in $FILES; do
  # Ejecuta comprobación de sintaxis
  python -m py_compile "$file"
  if [ $? -ne 0 ]; then
    echo "Error de sintaxis en $file. Por favor revisa y corrige."
    PASS=false
  fi
done

if ! $PASS; then
  exit 1
fi

exit 0
```

En este ejemplo, el hook iterará sobre todos los archivos Python (con extensión `.py`) que se estén a punto de ser committeados. Si se detecta un error de sintaxis al compilar el archivo, el commit se aborta y se solicita al desarrollador corregir los errores.

> **Consideración:** Es fundamental recordar que estos scripts deben ser ejecutables. Para ello, se debe modificar el permiso del archivo, por ejemplo:  
> `chmod +x .git/hooks/pre-commit`

##### **Commit-msg hook**

El hook `commit-msg` se utiliza para validar o modificar el mensaje del commit antes de que se registre en el historial. Por ejemplo, se puede configurar para asegurarse de que el mensaje cumpla con un determinado formato o longitud.

**Ejemplo de commit-msg hook en Bash:**

```bash
#!/bin/bash
# Este hook verifica que el mensaje de commit tenga al menos 15 caracteres

MSG_FILE=$1
MSG=$(cat "$MSG_FILE")

# Revisa la longitud del mensaje (sin contar espacios en blanco al inicio/final)
LENGTH=$(echo "$MSG" | sed 's/^ *//;s/ *$//' | wc -c)

if [ $LENGTH -lt 15 ]; then
  echo "El mensaje de commit es demasiado corto. Por favor, agrega más detalles."
  exit 1
fi

exit 0
```

Este hook impide que se realicen commits con mensajes demasiado breves, promoviendo así descripciones más claras y detalladas de los cambios realizados.

##### **Otros hooks relevantes**

- **Post-commit:** Se ejecuta después de que se ha completado un commit. Puede usarse para notificar a sistemas externos o actualizar estadísticas.
- **Pre-push:** Se ejecuta antes de enviar cambios a un repositorio remoto, permitiendo realizar validaciones de seguridad o integridad.

> **Ejemplo avanzado:** Integración de un hook que realice pruebas unitarias automáticamente. Antes de hacer push, se podría ejecutar un script que corra toda la batería de tests y solo permita el push si todas las pruebas pasan exitosamente. Esto se puede combinar con herramientas de integración continua para mejorar la robustez del repositorio.


### 2. Reescritura y limpieza de la historia

#### ¿Por qué reescribir la historia de Git?

Reescribir la historia puede ser necesario en varias situaciones, como:  
- **Remover información sensible:** Si se han agregado credenciales, contraseñas o datos que no deberían estar en el repositorio.
- **Limpiar commits innecesarios:** Para dejar un historial más coherente, eliminando commits innecesarios o combinando commits relacionados.
- **Renombrar archivos y directorios:** En algunos casos, es necesario actualizar nombres de archivos que se han usado por error.

Es importante destacar que reescribir la historia puede generar conflictos, especialmente cuando se trabaja en equipo, ya que altera los identificadores (hashes) de los commits. Por ello, estas acciones deben realizarse cuidadosamente y, de ser posible, aplicarse solo en ramas que aún no han sido publicadas.

#### git filter-branch

La herramienta `git filter-branch` permite reescribir la historia de un repositorio, aplicando filtros a cada commit. A pesar de ser muy poderosa, es conocida por su complejidad y, en repositorios grandes, puede resultar lenta y propensa a errores si no se utiliza adecuadamente.

**Ejemplo de uso: remover un archivo sensible**

Supongamos que se ha cometido el error de agregar un archivo llamado `secreto.txt` con información sensible. Para eliminar todos los rastros de este archivo del historial, se puede utilizar el siguiente comando:

```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch secreto.txt" \
  --prune-empty --tag-name-filter cat -- --all
```

- **Explicación:**
  - `--force`: Permite la reescritura sin confirmación.
  - `--index-filter`: Ejecuta un filtro en el índice para remover el archivo.
  - `--prune-empty`: Elimina los commits que queden vacíos tras la remoción.
  - `--tag-name-filter cat`: Actualiza los tags para mantener la coherencia.
  - `-- --all`: Aplica la acción a todas las ramas y tags.

Aunque `git filter-branch` es muy versátil, su complejidad y el riesgo de modificar de manera irreversible la historia han impulsado la adopción de herramientas alternativas más sencillas.

#### BFG Repo-Cleaner

BFG Repo-Cleaner es una herramienta más moderna y eficiente para limpiar y reescribir la historia en Git. Está diseñada específicamente para casos comunes, como la eliminación de archivos grandes o sensibles y ofrece una interfaz más amigable.

**Ejemplo de uso: remover archivos grandes o sensibles**

Si deseamos eliminar todos los archivos que superen cierto tamaño o que correspondan a patrones específicos (por ejemplo, todos los archivos de configuración con información sensible), se puede seguir este proceso:

1. **Descargar y preparar la herramienta BFG Repo-Cleaner:**  
   Visita el [sitio oficial de BFG](https://rtyley.github.io/bfg-repo-cleaner/) y descarga la versión correspondiente.

2. **Ejecutar BFG para limpiar el repositorio:**  
   Supongamos que queremos borrar todos los archivos llamados `passwords.txt`:

   ```bash
   java -jar bfg.jar --delete-files passwords.txt
   ```

   Este comando reescribe la historia, eliminando cada aparición del archivo `passwords.txt`. Una vez finalizado el proceso, es necesario ejecutar:

   ```bash
   git reflog expire --expire=now --all && git gc --prune=now --aggressive
   ```

   para limpiar de manera definitiva el repositorio y reducir el tamaño.

**Comparación entre git filter-branch y BFG Repo-Cleaner:**

- **Velocidad y facilidad de uso:**  
  BFG Repo-Cleaner es considerablemente más rápido y sencillo de utilizar para la mayoría de los casos comunes. Mientras que `git filter-branch` brinda un control muy detallado, su sintaxis es más compleja y es propenso a errores si no se emplea correctamente.

- **Casos de uso:**  
  Si el objetivo es una limpieza profunda o el manejo de casos muy particulares, `git filter-branch` puede ser la solución. Por otro lado, para eliminar archivos sensibles o grandes de manera rápida, BFG resulta ideal.

- **Seguridad y prevención de errores:**  
  Reescribir la historia puede romper la sincronización entre repositorios remotos y locales, por lo que se recomienda comunicar estos cambios a todos los colaboradores y, en algunos casos, forzar la actualización de ramas remotas tras la reescritura.


### 3. Git worktrees

#### ¿Qué es un worktree en Git?

Un worktree es una funcionalidad que permite tener múltiples directorios de trabajo (worktrees) vinculados a una misma estructura de repositorio. Esto es muy útil cuando se desea trabajar en varias ramas simultáneamente sin tener que cambiar de directorio o forzar la limpieza del área de trabajo actual.

#### Ventajas de utilizar worktrees

- **Paralelismo en el desarrollo:** Puedes trabajar en una rama de desarrollo y, a la vez, en otra rama destinada a pruebas o corrección de errores, cada una en su propio directorio.
- **Ahorro de tiempo y espacio:** Evitas la sobrecarga de clonar el mismo repositorio en diferentes ubicaciones. Los worktrees comparten la base de datos del repositorio, lo que mejora el rendimiento y ahorra espacio en disco.
- **Aislamiento de entrenamiento:** Permite aislar entornos de prueba o desarrollo, facilitando la experimentación sin afectar el estado principal de la rama.

#### Ejemplos prácticos de uso de worktrees

##### **Creación de un nuevo worktree**

Para crear un nuevo worktree y trabajar en una rama diferente, se puede utilizar el comando `git worktree add`. Supongamos que queremos trabajar en una nueva rama llamada `feature-x` en un directorio llamado `feature-x-worktree`:

```bash
# Crea la rama 'feature-x' y asocia un nuevo worktree
git worktree add -b feature-x ../feature-x-worktree origin/master
```

- **Explicación:**
  - `-b feature-x`: Crea una nueva rama basada en `origin/master`.
  - `../feature-x-worktree`: Es la ruta donde se creará el nuevo worktree. Se puede ajustar según la estructura del proyecto.
  - Con este comando, dispones de un área de trabajo independiente donde puedes implementar y probar nuevas funcionalidades.

##### **Listado y gestión de worktrees**

Para ver todos los worktrees asociados a un repositorio, basta con ejecutar:

```bash
git worktree list
```

Este comando muestra una lista con la ruta de cada worktree y la rama que está utilizando. Para eliminar (desasociar) un worktree que ya no se necesite, se usa:

```bash
git worktree remove ../feature-x-worktree
```

> **Nota:** Es importante asegurarse de que el worktree esté limpio (sin cambios pendientes) antes de eliminarlo, para evitar la pérdida accidental de trabajo.

##### Uso en un flujo de trabajo complejo

Imagina un escenario donde un desarrollador necesita trabajar en tres ramas de forma simultánea: la rama principal (`master` o `main`), una rama de desarrollo (`develop`) y una rama para una funcionalidad nueva (`feature-new`). Mediante el uso de worktrees, se podría configurar el entorno de la siguiente manera:

- **Worktree 1:** Directorio principal con la rama `master`.
- **Worktree 2:** Un directorio adicional para `develop`.
- **Worktree 3:** Otro directorio para `feature-new`.

Esto permite cambiar de contexto rápidamente, realizar pruebas cruzadas y comparar los estados de cada rama sin tener que ejecutar múltiples clones del repositorio.


### 4. Configuraciones y automatización avanzada

El manejo avanzado de Git no se limita a los comandos y funcionalidades básicas, sino que también abarca la personalización del entorno de trabajo mediante alias, configuraciones personalizadas y tareas de automatización. Estas técnicas facilitan el flujo de trabajo, reducen la cantidad de comandos repetitivos y ayudan a evitar errores humanos.

#### Alias y configuración personalizada

Los alias son atajos que se configuran en Git para ejecutar comandos de manera más rápida y abreviada. Se definen en el archivo de configuración global (`~/.gitconfig`) o en el de un repositorio específico (`.git/config`). Con alias se puede, por ejemplo, abreviar `git checkout` a `git co` o crear comandos compuestos que incluyan múltiples parámetros.

#### Ejemplos de alias comunes

A continuación se muestra un ejemplo de configuración de alias en el archivo `~/.gitconfig`:

```ini
[alias]
  co = checkout
  br = branch
  ci = commit
  st = status
  lg = log --oneline --graph --decorate --all
  amend = commit --amend
  unstage = reset HEAD --
```

- **Explicación:**
  - `co`, `br`, `ci`, `st`: Alias simples para comandos básicos.
  - `lg`: Un log que muestra la historia en formato resumido, con un gráfico de las ramas y la decoración de etiquetas.
  - `amend`: Permite modificar el último commit de forma rápida.
  - `unstage`: Facilita la acción de deshacer la selección de archivos (unstage).

#### Configuración personalizada

Además de los alias, Git permite configurar diversos parámetros para adaptar su comportamiento a las necesidades del equipo. Por ejemplo:

```ini
[color]
  ui = auto

[core]
  editor = vim
  autocrlf = input

[push]
  default = simple

[diff]
  tool = meld
```

- **Explicación:**
  - Se configura la interfaz de color para hacer más amigable la salida de los comandos.
  - Se elige `vim` como editor por defecto, aunque se puede cambiar según la preferencia del usuario.
  - `autocrlf` se configura para manejar diferencias en fin de línea en ambientes Unix y Windows.
  - Se establece el comportamiento por defecto al hacer push.
  - Se especifica una herramienta gráfica (en este caso, `meld`) para visualizar las diferencias entre commits.

#### Automatización en Git

La automatización en Git busca reducir tareas repetitivas y asegurar que ciertos procesos se realicen consistentemente, minimizando la posibilidad de errores. Esto se logra mediante:

- **Hooks automatizados:** Como vimos anteriormente, los hooks se pueden configurar para ejecutar tareas automáticas en respuesta a eventos.
- **Scripts de integración Continua (CI):** Integrar Git con servicios de CI/CD (por ejemplo, Jenkins, Travis CI, GitLab CI) para ejecutar pruebas, análisis de código y despliegues automáticos.
- **Tareas de mantenimiento programadas:** Por ejemplo, ejecutar scripts que limpien la base de datos del repositorio, verifiquen la integridad del mismo o actualicen documentación de manera automática.

#### Ejemplo de automatización con hooks y scripts

Imagina un escenario en el que se desea ejecutar una batería de pruebas unitarias cada vez que se realiza un `push`. Para ello, se puede configurar el hook `pre-push` de lasiguiente manera:

```bash
#!/bin/bash
# pre-push hook para ejecutar pruebas antes de enviar cambios

# Ejecuta los tests
./run_tests.sh
RESULT=$?

if [ $RESULT -ne 0 ]; then
  echo "Fallaron las pruebas unitarias. Aborto el push."
  exit 1
fi

exit 0
```

En este ejemplo, se asume que existe un script llamado `run_tests.sh` (por ahora considera los códigos anteriores)  en la raíz del repositorio, el cual ejecuta todas las pruebas unitarias. Si alguna de las pruebas falla (retornando un código diferente de cero), el script aborta el push, evitando así la integración de código que pueda romper la funcionalidad estable.

#### Automatización mediante aliases compuestos

Otro aspecto interesante de la automatización es la creación de alias compuestos que combinan varios comandos. Por ejemplo, se puede definir un alias que realice el `commit`, el `push` y, a continuación, lance una notificación o actualice una tarea en una herramienta de gestión.

**Ejemplo de alias compuesto en el archivo de configuración:**

```ini
[alias]
  quickpush = "!f() { git add -A && git commit -m \"$1\" && git push; }; f"
```

Con este alias, el usuario puede escribir:

```bash
git quickpush "Mensaje del commit"
```

El comando realiza de forma secuencial la adición de todos los archivos, realiza el commit con el mensaje proporcionado y ejecuta el push hacia el repositorio remoto. 
Este tipo de alias permite ahorrar tiempo y estandarizar procesos en el flujo de trabajo.

#### Automatización en configuraciones personalizadas con scripts

En ambientes empresariales o de gran escala, es común tener scripts que configuren automáticamente el entorno de Git en múltiples máquinas. Por ejemplo, se pueden desarrollar scripts en Bash o Python que:

- Instalen y configuren Git con los parámetros corporativos adecuados.
- Configuren hooks personalizados automáticamente en cada nuevo clon.
- Sincronicen configuraciones comunes (como alias o herramientas de diff) en todos los desarrolladores.

**Ejemplo de script de configuración automatizada:**

```bash
#!/bin/bash
# Script para configurar Git con ajustes corporativos

echo "Configurando Git..."
git config --global core.editor "vim"
git config --global color.ui auto
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --decorate --all"

# Configura hooks personalizados copiando el contenido de un directorio centralizado
HOOKS_DIR="$HOME/git-hooks"
REPO_HOOKS_DIR="$(git rev-parse --git-dir)/hooks"

if [ -d "$HOOKS_DIR" ]; then
  cp -r "$HOOKS_DIR"/* "$REPO_HOOKS_DIR"
  chmod +x "$REPO_HOOKS_DIR"/*
  echo "Hooks personalizados han sido configurados."
fi

echo "Configuración completada."
```

Este script configura ajustes globales y, además, copia hooks de un directorio central (`$HOME/git-hooks`) al directorio de hooks del repositorio actual, haciendo que todos
los desarrolladores utilicen los mismos scripts para tareas automatizadas.

> **Consejo de seguridad:** Siempre respalda y comunica cualquier cambio significativo en la configuración a todos los miembros del equipo, especialmente si se integran hooks y scripts que puedan modificar el flujo de trabajo de manera automatizada.

