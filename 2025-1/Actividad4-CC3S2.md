## **Actividad:** Introducción a Git - conceptos básicos y operaciones esenciales

### Objetivo de aprendizaje

Familiarizarse con los conceptos básicos de Git y realizar operaciones esenciales, como la configuración inicial, creación de repositorios, preparación y confirmación de cambios, visualización de historial, y gestión de ramas.

#### Conceptos básicos de Git: Comienza con una experiencia práctica

Antes de profundizar en los detalles, comencemos con una experiencia práctica. Es probable que sea más fácil comprender el concepto probándolo en lugar de solo leerlo al principio.


#### git config: Preséntate a Git

Ahora, hay algo que debes hacer antes de comenzar un proyecto. Preséntate a Git. Para presentarte a Git, usa el comando `git config`:

```bash
$ git config --global user.name "Kapumota"
$ git config --global user.email "kapumota@example.com"
```

`git config` es un comando utilizado para configurar Git a nivel de sistema, usuario y repositorio. El nivel *system* se aplica a todos los usuarios y a todos los repositorios. El nivel *global* se aplica a todos los repositorios de un usuario específico. El nivel *local* se aplica solo a un repositorio.

Para verificar que tu presentación se ha registrado, puedes comprobarlo con el comando `git config --list`:

```bash
$ git config --list

user.name=Your Name
user.email=Your Email
```

¡Ahora, la primera tarea está hecha! Pasemos rápidamente a las operaciones básicas de Git.


#### git init: Donde comienza tu viaje de código

Al igual que cada gran viaje tiene su origen, en el mundo de Git, el viaje de tu código comienza con el comando `git init`. El comando se usa para inicializar un nuevo repositorio de Git y comenzar a rastrear directorios existentes. Cuando ejecutas el comando, configura un directorio `.git` lleno de todo lo necesario para el control de versiones. Con eso fuera del camino, estás listo para sumergirte en la gama de comandos de Git y comenzar a rastrear y actualizar tu proyecto:

```bash
// Crea un directorio
$ mkdir kapumota-repo

// Cambia el directorio de trabajo actual
$ cd kapumota-repo/

$ git init
```

Otra forma es pasar un nombre de directorio como argumento, como `git init kapumota-repo`; esto creará el directorio, por lo que no necesitas ejecutar el comando `mkdir`.

Ahora que se ha creado el directorio `.git/`, los cambios en los archivos se guardan en el directorio `.git/`, pero Git no guarda automáticamente los archivos. En Git, *guardar* se completa ejecutando el comando `git add`, que selecciona conscientemente los archivos para guardar entre los que se han editado, agregado o eliminado, y el comando `git commit`, que registra esos cambios.

A continuación, agreguemos algo de código al repositorio.


#### git add: Preparando tu código

El comando `git add` es tu puente entre hacer cambios en tu directorio de trabajo y prepararlos para ser almacenados permanentemente en tu repositorio de Git. 
Cuando haces cambios en tus archivos, Git reconoce que estos archivos han cambiado, pero estos cambios no están automáticamente listos para convertirse en parte del historial. Aquí es donde entra `git add`. 

Primero, crea un nuevo archivo en tu directorio `kapumota-repo`:

```bash
// Crear un archivo README.md
$ echo " README" > README.md
```

El comando `git status` muestra el estado actual de tu repositorio, mostrando qué archivos tienen cambios que están siendo rastreados y cuáles no. Cuando ves el mensaje "*Untracked files*", es la forma de Git de informarte que hay un archivo del que aún no se le ha dicho que esté pendiente. 

En nuestro ejemplo, el archivo `README.md` es nuevo para Git y no está registrado; por lo tanto, está etiquetado como no rastreado:

```bash
// Verificando cómo Git reconoce el nuevo archivo
$ git status

On branch main
No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
    README.md
```

Los archivos recién agregados son parte de tu proyecto, pero no han sido rastreados por Git. Para moverlos del estado no rastreado a un estado rastreado, usa el comando `git add`:

```bash
$ git add README.md
$ git status

On branch main
No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
    new file:   README.m
```

Ahora Git reconoce `README.md` como un nuevo archivo y ahora está rastreado. El estado objetivo para guardar mediante el comando `git add` se llama *staged* (preparado). También puedes escuchar el término *índice* (index) utilizado indistintamente con *staging*. Antes de que los archivos o cambios sean preparados, residen en un área a menudo referida como el *espacio de trabajo* (workspace). Esta es esencialmente el entorno donde estás haciendo cambios activamente en tus archivos. 

Algunos también pueden referirse a esta área como el *árbol de trabajo* (worktree). En resumen, en este proceso, has preparado el archivo `README.md` desde el árbol de trabajo utilizando el comando `git add`.

**Importante**: `git add` tiene otras opciones también. Puedes incluir todo con `git add .`, incluir varios archivos como `git add file1.md file2.md file3.md`, o usar un comodín como `git add *.md` para agregar todos los archivos con la extensión `.md`.

Todo está en su lugar; es hora de registrar tus modificaciones en el historial.

#### git commit: registra cambios

El comando `git commit` registra los cambios que has preparado con `git add` en el historial del repositorio. Esto te permite rastrear cambios a lo largo del tiempo.

Imagina que estás jugando un videojuego desafiante. A medida que avanzas, a menudo guardarás tu juego para bloquear tus logros. Del mismo modo, cuando desarrollas software, guardarás tu trabajo usando `git commit`. Cada *commit* es un punto de guardado al que puedes regresar más tarde si es necesario.

Para cometer cambios, generalmente puedes hacer lo siguiente:

```bash
$ git commit -m "Initial commit with README.md
```

Aquí, la bandera `-m` es seguida por un mensaje corto y descriptivo que captura la esencia de los cambios que has hecho. Escribir buenos mensajes de *commit* es un arte, ya que ayuda a entender el historial y la intención de los cambios.

Ahora, usemos el comando `git status` nuevamente para ver si todos los cambios en el directorio de trabajo actual han sido guardados:

```bash
$ git status

On branch main
nothing to commit, working tree clean
```

Si aparece el mensaje "*nothing to commit*", tus cambios han sido incorporados.

Bueno, eso es todo; es muy fácil guardar un archivo en Git. Revisémoslo aquí. El flujo de edición, preparación y commit sigue siendo el mismo sin importar cuán complejo sea tu proyecto:

1. **Editar archivos**: Realiza los cambios necesarios en tus archivos. 

2. **Preparar cambios**: Decide qué archivos o cambios específicos te gustaría cometer y prepáralos. 

3. **Commit de cambios**: Una vez satisfecho con los cambios preparados, realiza un commit para registrarlos. Recuerda que cada commit genera una ID de commit única:


#### git log: Recorrer el árbol de commits

Una vez que hayas realizado algunos *commits*, es posible que desees retroceder y ver el historial de cambios realizados en el repositorio. Aquí es donde el comando `git log` resulta útil. El comando muestra una lista de *commits* realizados es un repositorio en orden cronológico inverso, es decir, el *commit* más reciente se muestra primero.

Para probar esto, usa el siguiente comando:

```bash
$ git log

commit a16e562c4cb1e4cc014220ec62f1182b3928935c (HEAD -> main)
Author: Kapumota <kapumota@example.com>
Date:   Thu Sep 28 16:30:00 2023 +0900

    Initial commit with README.md
```

Esto mostrará una lista de todos los *commits*, cada uno con lo siguiente:

- **Identificador SHA-1 único**: Actúa como una firma para el *commit* y puede emplearse en varios comandos de Git para referirse a ese *commit* específico.
- **Detalles del committer**: Muestra el nombre y el correo electrónico de la persona que realizó el *commit*.
- **Marca de tiempo (timestamp) del commit**: Muestra cuándo se realizó el *commit*.
- **Mensaje del commit**: Una nota breve e informativa que captura la esencia de las modificaciones en el *commit*.

Además del comando básico `git log`, hay numerosas opciones que te permiten adaptar la salida a tus necesidades:

- `git log -p`: Muestra la diferencia (es decir, el parche) introducida en cada *commit*.
- `git log --stat`: Proporciona algunas estadísticas abreviadas para cada *commit*.
- `git log --oneline`: Da una salida más compacta, mostrando cada *commit* como una sola línea.
- `git log --graph`: Visualiza la historia de *ramas* y *merges* en un diseño de gráfico ASCII.
- `git log --author="Kapumota"`: Filtra los *commits* para mostrar solo los realizados por una persona específica (en este caso, "Kapumota").

Por ejemplo, también puede mejorar la perspectiva de la siguiente manera:

```bash
$ git log --graph --pretty=format:'%x09 %h %ar ("%an") %s'
```

**Pregunta**: ¿Cual es la salida de este comando?

**Pregunta**: Intentemos el comando `git log` en este ejercicio (puedes realizar otra cosa como colocar las cosas en español). Primero, actualiza el archivo `README.md` y crea un nuevo archivo `CONTRIBUTING.md`:

```bash
$ echo " CONTRIBUTING" > CONTRIBUTING.md
$ echo " README\n\nWelcome to the project" > README.md
$ git add .
$ git commit -m "Set up the repository base documentation"
```

Una vez hecho, agrega un código de ejemplo en Python:

```bash
$ echo "print('Hello World')" > main.py
$ git add .
$ git commit –m "Add main.py"
```

Cuando se confirme en el *log* que está correctamente registrado, está hecho:

```bash
$ git log --oneline

344a02a (HEAD -> main) Add main.py
b641640 Set up the repository base documentation
a16e562 Initial commit with README.md
```

En esencia, el comando `git log` es una herramienta vital para cualquier desarrollador. Te ayuda a navegar fácilmente a través del historial de tu código, ya sea que estés buscando un cambio específico o simplemente revisando el trabajo anterior.

---

### Trabajar con ramas: La piedra angular de la colaboración

Mientras que las secciones anteriores te proporcionan una comprensión sólida de cómo inicializar y gestionar un repositorio de Git, el concepto de *branching* lleva esto a un nuevo nivel. Mientras que acumular `git commit` solo crea un historial lineal, `git branch` se puede usar para crear un historial del entorno paralelo. Luego, puedes fusionar esos múltiples entornos en uno, lo que permite que varias personas trabajen en ellos, dándote la flexibilidad para experimentar con nuevas características, correcciones de errores o incluso ideas totalmente vanguardistas sin afectar la base de código principal.


#### git branch: Entendiendo los conceptos básicos de Git branch

Cuando inicializas un repositorio de Git, automáticamente crea una *rama (branch)* predeterminada, generalmente llamada `main` (anteriormente conocida como `master`). Cuando ejecutas el comando `git branch`, mostrará la lista de todas las *ramas* en tu repositorio, con la *branch* actual destacada:

```bash
$ git branch
* main
```

Puedes crear una nueva *rama* con el comando `git branch <branch name>`. Este comando crea una nueva *rama* a partir de la *rama* actual:

```bash
$ git branch feature/new-feature
```

Si creas una nueva *rama*, puedes construir una línea con un historial diferente y agregar *commits* a esa *rama*.

Las convenciones de nombres de *ramas* son importantes para la comunicación. Un estándar comúnmente utilizado es anteponer el nombre de la *rama* con `feature/`, `bugfix/` o `hotfix/`, seguido de una breve descripción. Esto facilita que cualquiera entienda el propósito de la *branch* de un vistazo.

También puedes crear una *rama* a partir de una *rama* o *commit* específico que sea diferente al que estás trabajando actualmente. Esto es particularmente útil cuando necesitas crear una *rama* de característica (feature) o corrección de errores (bugfix) que debería originarse desde una *rama* de desarrollo o *staging* designada en lugar de desde tu *branch* de trabajo actual:

```bash
// Crear una rama desde una rama específica
$ git branch <new-branch-name> <base-branch-name>

// Crear una rama desde un commit específico
$ git branch <new-branch-name> <commit-hash>
```

#### git checkout/git switch: Cambiar entre ramas

En tu flujo de trabajo diario, a menudo necesitarás cambiar de una *rama* a otra, especialmente cuando trabajas en múltiples características o corrigiendo errores. Cuando hayas comenzado a trabajar en múltiples *ramas*, volverse consciente de la *branch* en la que estás activamente se vuelve fundamental. En Git, el término *HEAD* se refiere a la punta de la *rama* con la que estás trabajando activamente.

Cambiar tu *rama* de trabajo actual se conoce como cambiar a una *rama*. El comando `git checkout` facilita esto:

```bash
// Cambiar a la rama 'feature/new-feature'
$ git checkout feature/new-feature
```

Esta operación cambia la posición de HEAD, la punta de la *rama*, a una *rama* llamada `feature/new-feature`:

El comando `git checkout` da como resultado que la posición actual sea el *commit* en la punta de la *rama* `feature/new-feature`, es decir, HEAD.

#### Ejemplos adicionales

#### Crear una rama desde una rama específica
```bash
// Verifica en qué rama estás actualmente
$ git branch

// Cambia a la rama 'develop' si no estás en ella
$ git checkout develop

// Crea una nueva rama 'feature/login' desde 'develop'
$ git branch feature/login develop

// Cambia a la nueva rama 'feature/login'
$ git checkout feature/login
```

#### Crear una rama desde un commit específico
```bash
// Verifica el historial de commits para identificar el commit específico
$ git log --oneline

// Crear una nueva rama 'hotfix/bugfix' basada en el commit 'abc1234'
$ git branch hotfix/bugfix abc1234

// Cambia a la nueva rama 'hotfix/bugfix'
$ git checkout hotfix/bugfix
```

Las versiones recientes de Git también ofrecen el comando `git switch`, que proporciona una forma más intuitiva de cambiar *ramas*:

```bash
// Cambiar a la rama 'feature/new-feature'
$ git switch feature/new-feature
```

A veces, puede resultar eficiente crear una nueva *rama* y cambiar a ella inmediatamente. Git proporciona un comando abreviado para esto, que combina la funcionalidad de `git branch` y `git checkout` o `git switch`.

Para crear una nueva *rama* y cambiar a ella en un solo paso, puedes usar el comando `git checkout -b`:

```bash
// Crear y cambiar a una nueva rama
$ git checkout -b feature/another-new-feature
```

Esto es equivalente a ejecutar lo siguiente:

```bash
$ git branch feature/another-new-feature
$ git checkout feature/another-new-feature
```

En las versiones recientes de Git, puedes lograr lo mismo con `git switch` usando la opción `-c`:

```bash
// Crear y cambiar a una nueva rama
$ git switch -c feature/another-new-feature
```


#### git merge <Branch Name>: Fusionando ramas

Una vez que hayas realizado cambios en una *rama* y los hayas probado a fondo, es posible que desees integrar esos cambios nuevamente en la *branch* `main` u otra *rama*. Esta operación se conoce como *merge* (fusión):

```bash
// Primero, cambia a la rama en la que deseas fusionar
$ git checkout main

// Ahora, fusiona tu rama de características
$ git merge feature/new-feature
```

La fusión te permite fusionar líneas con diferentes historiales. La fusión puede ser una operación sencilla, pero también puede complicarse si hay conflictos entre las *ramas*. 

En tales casos, Git requerirá intervención manual para resolver los conflictos. 


#### git branch -d: Eliminando una rama

Una vez que una *rama* ha sido fusionada con éxito y ya no es necesaria, se puede eliminar para mantener limpio el repositorio:

```bash
// Eliminar una rama local
$ git branch -d feature/new-feature
```

#### Preguntas

- ¿Cómo te ha ayudado Git a mantener un historial claro y organizado de tus cambios?  
- ¿Qué beneficios ves en el uso de ramas para desarrollar nuevas características o corregir errores?  
- Realiza una revisión final del historial de commits para asegurarte de que todos los cambios se han registrado correctamente.  
- Revisa el uso de ramas y merges para ver cómo Git maneja múltiples líneas de desarrollo.

#### Ejercicios

##### Ejercicio 1: Manejo avanzado de ramas y resolución de conflictos

**Objetivo:** Practicar la creación, fusión y eliminación de ramas, así como la resolución de conflictos que puedan surgir durante la fusión.

**Instrucciones:**

1. **Crear una nueva rama para una característica:**
   - Crea una nueva rama llamada `feature/advanced-feature` desde la rama `main`:

     ```bash
     $ git branch feature/advanced-feature
     $ git checkout feature/advanced-feature
     ```

2. **Modificar archivos en la nueva rama:**
   - Edita el archivo `main.py` para incluir una función adicional:
     ```python
     def greet():
         print('Hello from advanced feature')

     greet()
     ```
   - Añade y confirma estos cambios en la rama `feature/advanced-feature`:

     ```bash
     $ git add main.py
     $ git commit -m "Add greet function in advanced feature"
     ```

3. **Simular un desarrollo paralelo en la rama main:**
   - Cambia de nuevo a la rama `main`:

     ```bash
     $ git checkout main
     ```
   - Edita el archivo `main.py` de forma diferente (por ejemplo, cambia el mensaje del print original):
     ```python
     print('Hello World - updated in main')
     ```
   - Añade y confirma estos cambios en la rama `main`:

     ```bash
     $ git add main.py
     $ git commit -m "Update main.py message in main branch"
     ```

4. **Intentar fusionar la rama feature/advanced-feature en main:**
   - Fusiona la rama `feature/advanced-feature` en `main`:

     ```bash
     $ git merge feature/advanced-feature
     ```

5. **Resolver el conflicto de fusión:**
   - Git generará un conflicto en `main.py`. Abre el archivo y resuelve el conflicto manualmente, eligiendo cómo combinar las dos versiones.
   - Después de resolver el conflicto, añade el archivo resuelto y completa la fusión:

     ```bash
     $ git add main.py
     $ git commit -m "Resolve merge conflict between main and feature/advanced-feature"
     ```

6. **Eliminar la rama fusionada:**
   - Una vez que hayas fusionado con éxito y resuelto los conflictos, elimina la rama `feature/advanced-feature`:

     ```bash
     $ git branch -d feature/advanced-feature
     ```


#### Ejercicio 2: Exploración y manipulación del historial de commits

**Objetivo:** Aprender a navegar y manipular el historial de commits usando comandos avanzados de Git.

**Instrucciones:**

1. **Ver el historial detallado de commits:**
   - Usa el comando `git log` para explorar el historial de commits, pero esta vez con más detalle:

     ```bash
     $ git log -p
     ```
   - Examina las diferencias introducidas en cada commit. ¿Qué cambios fueron realizados en cada uno?

2. **Filtrar commits por autor:**
   - Usa el siguiente comando para mostrar solo los commits realizados por un autor específico:

     ```bash
     $ git log --author="TuNombre"
     ```

3. **Revertir un commit:**
   - Imagina que el commit más reciente en `main.py` no debería haberse hecho. Usa `git revert` para revertir ese commit:

     ```bash
     $ git revert HEAD
     ```
   - Verifica que el commit de reversión ha sido añadido correctamente al historial.

4. **Rebase interactivo:**
   - Realiza un rebase interactivo para combinar varios commits en uno solo. Esto es útil para limpiar el historial de commits antes de una fusión.
   - Usa el siguiente comando para empezar el rebase interactivo:

     ```bash
     $ git rebase -i HEAD~3
     ```
   - En el editor que se abre, combina los últimos tres commits en uno solo utilizando la opción `squash`.

5. **Visualización gráfica del historial:**
   - Usa el siguiente comando para ver una representación gráfica del historial de commits:

     ```bash
     $ git log --graph --oneline --all
     ```
   - Reflexiona sobre cómo el historial de tu proyecto se visualiza en este formato. ¿Qué información adicional puedes inferir?


#### Ejercicio 3: Creación y gestión de ramas desde commits específicos

**Objetivo:** Practicar la creación de ramas desde commits específicos y comprender cómo Git maneja las referencias históricas.

**Instrucciones:**

1. **Crear una nueva rama desde un commit específico:**
   - Usa el historial de commits (`git log --oneline`) para identificar un commit antiguo desde el cual crear una nueva rama:

     ```bash
     $ git log --oneline
     ```
   - Crea una nueva rama `bugfix/rollback-feature` desde ese commit:

     ```bash
     $ git branch bugfix/rollback-feature <commit-hash>
     $ git checkout bugfix/rollback-feature
     ```

2. **Modificar y confirmar cambios en la nueva rama:**
   - Realiza algunas modificaciones en `main.py` que simulen una corrección de errores:
     ```python
     def greet():
         print('Fixed bug in feature')
     ```
   - Añade y confirma los cambios en la nueva rama:

     ```bash
     $ git add main.py
     $ git commit -m "Fix bug in rollback feature"
     ```

3. **Fusionar los cambios en la rama principal:**
   - Cambia de nuevo a la rama `main` y fusiona la rama `bugfix/rollback-feature`:

     ```bash
     $ git checkout main
     $ git merge bugfix/rollback-feature
     ```

4. **Explorar el historial después de la fusión:**
   - Usa `git log` y `git log --graph` para ver cómo se ha integrado el commit en el historial:

     ```bash
     $ git log --graph --oneline
     ```

5. **Eliminar la rama bugfix/rollback-feature:**
   - Una vez fusionados los cambios, elimina la rama `bugfix/rollback-feature`:

     ```bash
     $ git branch -d bugfix/rollback-feature
     ```


#### Ejercicio 4: Manipulación y restauración de commits con git reset y git restore

**Objetivo:** Comprender cómo usar `git reset` y `git restore` para deshacer cambios en el historial y en el área de trabajo.

**Instrucciones:**

1. **Hacer cambios en el archivo main.py:**
   - Edita el archivo `main.py` para introducir un nuevo cambio:
     ```python
     print('This change will be reset')
     ```
   - Añade y confirma los cambios:

     ```bash
     $ git add main.py
     $ git commit -m "Introduce a change to be reset"
     ```

2. **Usar git reset para deshacer el commit:**
   - Deshaz el commit utilizando `git reset` para volver al estado anterior:

     ```bash
     $ git reset --hard HEAD~1
     ```
   - Verifica que el commit ha sido eliminado del historial y que el archivo ha vuelto a su estado anterior.

3. **Usar git restore para deshacer cambios no confirmados:**
   - Realiza un cambio en `README.md` y no lo confirmes:

     ```bash
     $ echo "Another line in README" >> README.md
     $ git status
     ```
   - Usa `git restore` para deshacer este cambio no confirmado:

     ```bash
     $ git restore README.md
     ```
   - Verifica que el cambio no confirmado ha sido revertido.


#### Ejercicio 5: Trabajo colaborativo y manejo de Pull Requests

**Objetivo:** Simular un flujo de trabajo colaborativo utilizando ramas y pull requests.

**Instrucciones:**

1. **Crear un nuevo repositorio remoto:**
   - Usa GitHub o GitLab para crear un nuevo repositorio remoto y clónalo localmente:

     ```bash
     $ git clone <URL-del-repositorio>
     ```

2. **Crear una nueva rama para desarrollo de una característica:**
   - En tu repositorio local, crea una nueva rama `feature/team-feature`:

     ```bash
     $ git branch feature/team-feature
     $ git checkout feature/team-feature
     ```

3. **Realizar cambios y enviar la rama al repositorio remoto:**
   - Realiza cambios en los archivos del proyecto y confírmalos:

     ```bash
     $ echo "print('Collaboration is key!')" > collaboration.py
     $ git add .
     $ git commit -m "Add collaboration script"
     ```
   - Envía la rama al repositorio remoto:

     ```bash
     $ git push origin feature/team-feature
     ```

4. **Abrir un Pull Request:**
   - Abre un Pull Request (PR) en la plataforma remota (GitHub/GitLab) para fusionar `feature/team-feature` con la rama `main`.
   - Añade una descripción detallada del PR, explicando los cambios realizados y su propósito.

5. **Revisar y fusionar el Pull Request:**
   - Simula la revisión de código, comenta en el PR y realiza cualquier cambio necesario basado en la retroalimentación.
   - Una vez aprobado, fusiona el PR en la rama `main`.

6. **Eliminar la rama remota y local:**
   - Después de la fusión, elimina la rama tanto local como remotamente:

     ```bash
     $ git branch -d feature/team-feature
     $ git push origin --delete feature/team-feature
     ```

#### Ejercicio 6: Cherry-Picking y Git Stash

**Objetivo:** Aprender a aplicar commits específicos a otra rama utilizando `git cherry-pick` y a guardar temporalmente cambios no confirmados utilizando `git stash`.

**Instrucciones:**

1. **Hacer cambios en main.py y confirmarlos:**
   - Realiza y confirma varios cambios en `main.py` en la rama `main`:

     ```bash
     $ echo "print('Cherry pick this!')" >> main.py
     $ git add main.py
     $ git commit -m "Add cherry-pick example"
     ```

2. **Crear una nueva rama y aplicar el commit específico:**
   - Crea una nueva rama `feature/cherry-pick` y aplícale el commit específico:

     ```bash
     $ git branch feature/cherry-pick
     $ git checkout feature/cherry-pick
     $ git cherry-pick <commit-hash>
     ```

3. **Guardar temporalmente cambios no confirmados:**
   - Realiza algunos cambios en `main.py` pero no los confirmes:

     ```bash
     $ echo "This change is stashed" >> main.py
     $ git status
     ```
   - Guarda temporalmente estos cambios utilizando `git stash`:

     ```bash
     $ git stash
     ```

4. **Aplicar los cambios guardados:**
   - Realiza otros cambios y confírmalos si es necesario.
   - Luego, recupera los cambios guardados anteriormente:

     ```bash
     $ git stash pop
     ```

5. **Revisar el historial y confirmar la correcta aplicación de los cambios:**
   - Usa `git log` para revisar el historial de commits y verificar que todos los cambios se han aplicado correctamente.
